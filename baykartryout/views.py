from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Part, PlaneType, Department, Assembly, UsedPart, PartModel, UserCred
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm

def loginPage(request):
    page= 'login_page'

    if request.user.is_authenticated:
        return redirect('part_create')
    else:
        print(request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username', '').lower()
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not exist')

        user = authenticate(username=username, password=password)
        department = UserCred.objects.filter(user = user)

        if user is not None:
            user_cred = UserCred.objects.filter(user=user).first()
            department = user_cred.department
            print(department)
            if department == "Kanat Takimi":
                login(request, user)
                messages.success(request, "Giriş Yaptınız")
                return redirect('part_list')
            elif department == "Gövde Takimi":
                login(request, user)
                messages.success(request, "Giriş Yaptınız")
                return redirect('part_list')
            elif department == "Kuyruk Takimi":
                login(request, user)
                messages.success(request, "Giriş Yaptınız")
                return redirect('part_list')
            elif department == "Aviyonik Takimi":
                login(request, user)
                messages.success(request, "Giriş Yaptınız")
                return redirect('part_list')
            elif department == "Montaj Takimi":
                login(request, user)
                messages.success(request, "Giriş Yaptınız")
                return redirect('assembly_list')
            else:
                messages.warning(request, 'Geçersiz Bilgiler')
                return redirect('login_page')
        else:
            messages.warning(request, 'Geçersiz Bilgiler')
            return redirect('login_page')
        
    context = {'page': page}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login_page')

def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kullanıcı başarıyla oluşturuldu!")
            return redirect('login_page')

    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login')
def part_list(request):
    parts = Part.objects.filter(quantity__gt=0)
    return render(request, 'part_list.html', {'parts': parts})

@login_required(login_url='/login')
def part_create(request):

    user_department = UserCred.objects.filter(user=request.user).first().department


    department_part_choices = {
        Department.KANAT_TAKIMI: PartModel.KANAT,
        Department.GOVDE_TAKIMI: PartModel.GOVDE,
        Department.KUYRUK_TAKIMI: PartModel.KUYRUK,
        Department.AVIYONIK_TAKIMI: PartModel.AVIYONIK,
    }

    if request.method == "POST":
        part_name = request.POST.get("part_name")
        plane_type = request.POST.get("plane_type")
        department = request.POST.get("department")
        quantity = request.POST.get("quantity")

        if department != user_department:
            messages.error(request, f"{user_department} departmanına ait olmayan bir parça oluşturamazsınız.")
            print(request, f"{user_department} departmanına ait olmayan bir parça oluşturamazsınız.")
            return redirect('part_create')
        
        if part_name != department_part_choices.get(department):
            messages.error(request, f"{department} departmanına ait geçerli bir parça seçmelisiniz.")
            print(request, f"{department} departmanına ait geçerli bir parça seçmelisiniz.")
            return redirect('part_create')

        Part.objects.create(part_name=part_name, plane_type=plane_type, department=department, quantity=quantity)
        messages.success(request, f"{part_name} parçası başarıyla eklendi.")
        return redirect('part_list')
    
    part_names = PartModel.choices
    plane_types = PlaneType.choices
    departments = [choice for choice in Department.choices if choice[0] != Department.MONTAJ_TAKIMI]
    user_department = user_department
    return render(request, 'part_create.html', {'part_names': part_names, 'plane_types': plane_types, 'departments': departments, 'user_department': user_department})

@login_required(login_url='/login')
def assembly_create(request):
    # Sadece Montaj Takımı'na izin verilmesi
    user_department = UserCred.objects.filter(user=request.user).first().department
    if user_department != 'Montaj Takimi':
        return redirect('part_list')

    if request.method == "POST":
        plane_type = request.POST.get("plane_type")
        assembly = Assembly.objects.create(plane_type=plane_type)

        required_parts = {
            Department.KANAT_TAKIMI: 2,
            Department.GOVDE_TAKIMI: 1,
            Department.KUYRUK_TAKIMI: 1,
            Department.AVIYONIK_TAKIMI: 1
        }

        used_parts_count = {
            Department.KANAT_TAKIMI: 0,
            Department.GOVDE_TAKIMI: 0,
            Department.KUYRUK_TAKIMI: 0,
            Department.AVIYONIK_TAKIMI: 0
        }

        for department, required_quantity in required_parts.items():
            parts = Part.objects.filter(plane_type=plane_type, department=department)
            total_available = sum(part.quantity for part in parts)
            if total_available < required_quantity:
                messages.error(request, f"{department} için yeterli parça stoğu yok! Gerekli: {required_quantity}, Mevcut: {total_available}")
                assembly.delete()
                return redirect('assembly_create')

            for part in parts:
                if required_quantity <= 0:
                    break
                use_quantity = min(part.quantity, required_quantity)
                used_parts_count[department] += use_quantity
                UsedPart.objects.create(assembly=assembly, part=part, quantity_used=use_quantity)
                part.quantity -= use_quantity
                part.save()
                required_quantity -= use_quantity

        print("Kullanılan parçalar:", used_parts_count)
        return redirect('assembly_list')
    
    plane_types = PlaneType.choices
    parts = Part.objects.all()
    return render(request, 'assembly_create.html', {'plane_types': plane_types, 'parts': parts})

@login_required(login_url='/login')
def assembly_list(request):
    user_department = UserCred.objects.filter(user=request.user).first().department
    if user_department != 'Montaj Takimi':
        return redirect('part_list')
    
    assemblies = Assembly.objects.all()
    assembly_details = []

    for assembly in assemblies:
        used_parts = assembly.used_parts.all()
        part_count = {
            Department.KANAT_TAKIMI: 0,
            Department.GOVDE_TAKIMI: 0,
            Department.KUYRUK_TAKIMI: 0,
            Department.AVIYONIK_TAKIMI: 0
        }
        for used_part in used_parts:
            part_count[used_part.part.department] += used_part.quantity_used
        
        assembly_details.append({
            'assembly': assembly,
            'part_count': part_count
        })
    return render(request, 'assembly_list.html', {'assembly_details': assembly_details})

def deletePart(request, pk):
    part = Part.objects.get(id=pk)
    if request.method == 'POST':
        part.delete()
        messages.success(request, f"{part.part_name} başarıyla silindi.")
        return redirect('part_list')
    return render(request, 'delete.html', {'obj': part})