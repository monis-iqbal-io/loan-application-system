from django.shortcuts import render, redirect
from .forms import Step1Form , Step2Form , Step3Form , Step4Form
from .models import LoanApplication
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

fs = FileSystemStorage(location=settings.MEDIA_ROOT)

def home_view(request):
    return render(request, 'home.html')

def step1_view(request):

    if request.method == "GET" and 'step1' not in request.session:
        request.session.flush()
    
    if request.method == 'POST':
        form = Step1Form(request.POST)

        if form.is_valid():
            # store data in session
            data = form.cleaned_data.copy()

            # convert decimal to float 
            data['loan_amount'] = float(data['loan_amount'])

            request.session['step1'] = data

            print("session data:" , request.session['step1'])
            return redirect('step2')
        
    else:
        # when the user revisits the page , prefil the form with session data
        session_data = request.session.get('step1')

        if session_data:
            form = Step1Form(initial=session_data)
        else:
            form = Step1Form()

    return render(request , 'step1.html' , {'form': form})


def step2_view(request):
    #  Ensure step1 is completed

    if 'step1' not in request.session:
        return redirect('step1')
    
    if request.method == 'POST':
        form = Step2Form(request.POST)

        if form.is_valid():
            request.session['step2'] = form.cleaned_data

            print("STEP 2 SESSION:" , request.session['step2'])

            return redirect('step3')
    
    else:
        # prefill data id user revisits the page
        session_data = request.session.get('step2')

        if session_data:
            form = Step2Form(initial=session_data)
        else:
            form = Step2Form()

    return render(request , 'step2.html' , {'form': form})


def step3_view(request):

    #Ensure Step 2 is completed
    if 'step2' not in request.session:
        return redirect('step1')

    if request.method == "POST":
        form = Step3Form(request.POST)

        if form.is_valid():

            data = form.cleaned_data.copy()

            #Convert Decimal to float
            data['monthly_income'] = float(data['monthly_income'])

            request.session['step3'] = data

            print("STEP 3 SESSION:", request.session['step3'])

            return redirect('step4')  

    else:
        # prefill data if user revisits the page
        session_data = request.session.get('step3')

        if session_data:
            form = Step3Form(initial=session_data)
        else:
            form = Step3Form()

    return render(request, 'step3.html', {'form': form})


def step4_view(request):

    #Ensure Step 3 is completed
    if 'step3' not in request.session:
        return redirect('step1')

    if request.method == "POST":
        form = Step4Form(request.POST, request.FILES)

        if form.is_valid():

            fs = FileSystemStorage(location=settings.MEDIA_ROOT)

            # save files physically
            profile_photo_file = request.FILES.get('profile_photo')
            profile_photo_name = fs.save(profile_photo_file.name, profile_photo_file)
           
            id_proof_file = request.FILES.get('id_proof')
            id_proof_name = fs.save(id_proof_file.name, id_proof_file)

            optional_doc_file = request.FILES.get('optional_doc')
            optional_doc_name = None        

            if optional_doc_file:
                optional_doc_name = fs.save(optional_doc_file.name, optional_doc_file)  

            # store file paths in session
            request.session['step4'] = {
                'profile_photo': profile_photo_name,    
                'id_proof': id_proof_name,
                'optional_doc': optional_doc_name
            }

            return redirect('preview') 

    else:
        form = Step4Form()

    return render(request, 'step4.html', {'form': form})



def preview_view(request):

    # ensure all steps are completed

    required_steps = ['step1', 'step2', 'step3', 'step4']

    for step in required_steps:
        if step not in request.session:
            return redirect('step1')
        
    # Collect all data step by step

    step1 = request.session.get('step1',{})
    step2 = request.session.get('step2',{})
    step3 = request.session.get('step3',{})
    step4 = request.session.get('step4',{})

    # merge all data

    data = {
        **step1,
        **step2,
        **step3,
        **step4
     }
    
    return render(request, 'preview.html', {'data': data})


from .models import LoanApplication

def submit_view(request):

    if request.method == "POST":

        #Ensure all steps completed
        required_steps = ['step1', 'step2', 'step3', 'step4']
        for step in required_steps:
            if step not in request.session:
                return redirect('step1')

        # Collect all data
        step1 = request.session.get('step1', {})
        step2 = request.session.get('step2', {})
        step3 = request.session.get('step3', {})
        step4 = request.session.get('step4', {})

        data = {
            **step1,
            **step2,
            **step3,
        }

        # Duplicate Check
        if LoanApplication.objects.filter(phone=data.get('phone')).exists(): 
            messages.error(request, "A loan application with this phone number already exists.")
            return redirect('step1')

        # handle files
        step4 = request.session.get('step4', {})
        profile_photo_name = step4.get('profile_photo')
        id_proof_name = step4.get('id_proof')       
        optional_doc_name = step4.get('optional_doc') 

        # Save to Database
        LoanApplication.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),

            loan_amount=data.get('loan_amount'),
            tenure=data.get('tenure'),

            address_line1=data.get('address_line1'),
            address_line2=data.get('address_line2'),
            city=data.get('city'),
            state=data.get('state'),
            pincode=data.get('pincode'),

            employment_type=data.get('employment_type'),
            company_name=data.get('company_name'),
            monthly_income=data.get('monthly_income'),
            work_experience=data.get('work_experience'),

            profile_photo=profile_photo_name,
            id_proof=id_proof_name,
            optional_doc=  optional_doc_name if optional_doc_name else None
        )

        # Clear Session
        request.session.flush()

        return redirect('thank_you')

    return redirect('step1')


def thank_you_view(request):
    return render(request, 'thank_you.html')