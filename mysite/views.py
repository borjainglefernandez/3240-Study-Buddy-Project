# Watkins, jmw4dx
from django.http import HttpResponseRedirect, HttpResponse
from studentprofile.models import Student, Schedule, Course, Class
from django.contrib.auth.models import User
from django.views import generic
from django.shortcuts import render, reverse
from studygroups.models import StudyGroup

# Creates a local variable containing all the UVa majors
majors = ["Undeclared",
                "Aerospace Engineering",
                "African American and African Studies",
                "American Studies",
                "Anthropology",
                "Archaeology",
                "Architectural History",
                "Architecture",
                "Astronomy",
                "Bachelor of Interdisciplinary Studies",
                "Bachelor of Professional Studies in Health Sciences Management",
                "Biology",
                "Biomedical Engineering",
                "Chemical Engineering",
                "Chemistry",
                "Civil Engineering",
                "Classics",
                "Cognitive Science",
                "Commerce",
                "Comparative Literature",
                "Computer Engineering",
                "Computer Science (B.A.)",
                "Computer Science (B.S.)",
                "Dance",
                "Drama",
                "East Asian Languages, Literatures and Culture",
                "Economics",
                "Electrical Engineering",
                "Engineering Science",
                "English",
                "Environmental Sciences",
                "Environmental Thought and Practice",
                "Five-Year Teacher Education Program",
                "French",
                "German",
                "German Studies",
                "Global Studies",
                "Global Sustainability Minor",
                "Historic Preservation Minor",
                "History",
                "History of Art",
                "Human Biology",
                "Interdisciplinary Major of Global Studies",
                "Jewish Studies",
                "Kinesiology(BSEd)",
                "Latin American Studies",
                "Linguistics",
                "Materials Science and Engineering",
                "Mathematics",
                "Mechanical Engineering",
                "Media Studies",
                "Medieval Studies",
                "Middle Eastern Language & Literature",
                "Middle East Studies",
                "Music",
                "Neuroscience",
                "Nursing",
                "Philosophy",
                "Physics",
                "Political and Social Thought",
                "Political Philosophy, Policy, and Law",
                "Politics",
                "Psychology",
                "Religious Studies",
                "Slavic Languages and Literatures",
                "Sociology",
                "South Asian Language & Literature",
                "South Asian Studies",
                "Spanish",
                "Speech Communication Disorders",
                "Statistics",
                "Studio Art",
                "Systems Engineering"
                "Urban and Environmental Planning",
                "Women, Gender & Sexuality",
                "Youth & Social Innovation(BSEd)"
                ]

def home(request):
    return HttpResponse("Hello, world! You're at the site.")

def submit_profile(request):
    try:
        user = User.objects.get(pk=request.user.id) # Fetch the current user
    except:
        return HttpResponseRedirect(reverse('home'))

    # Error for if user name is null and its the first time the user is logging in
    null_name_error_create = render(request, 'studentprofile.html', { # Redirects the user to the login page again
        'error_message': "Username cannot be blank.", # Description for the error message displayed
        'get_majors': majors,
    })

    # Error for if user name is null and the user is editing their profile
    null_name_error_edit = render(request, 'studentprofile.html', {  # Redirects the user to the profile page again
        'error_message': "Username cannot be blank.",  # Description for the error message displayed
        'get_majors': majors,
    })

    # Error for if user name is null and the user is editing their profile
    phone_error_edit = render(request, 'studentprofile.html', {  # Redirects the user to the profile page again
        'error_message': "Phone numbers must be 10-digits with no special characters",  # Description for the error message displayed
        'get_majors': majors,
    })

    if request.method=='POST':
        first_time = False
        print(request.POST)

        try:
            student = Student.objects.get(user=request.user)

            if request.POST["Name"].strip() == "":
                return null_name_error_edit # if user is editing their profile and there is no name
                                            # raise the error
            number = request.POST["phone"]
            hyphen = '-' in number
            openP = '(' in number
            closeP = ')' in number
            defaultNum = number == 5551234567 or number == 0
            numLength = len(str(number)) != 10
            
            if hyphen or openP or closeP or defaultNum or numLength:
                return phone_error_edit
        except:
            if request.POST["Name"].strip() == "":
                return null_name_error_create # if user is creating their profile for first time and there is no name
                                              # raise the error
            # Create a Student Object that connects to that user
            student = Student(user = user, name = request.POST['Name'], year = request.POST['Year'],
                        major = request.POST['Major'], num = request.POST['NumClass'], phone = request.POST['phone'])
            first_time = True
            # Save the Student Object we have just created
            student.save()


        # If this is the first time the user is generating the schedule
        if 'generate-schedule' in request.POST and first_time:

            # Create an array equivalent to the size of the number of classes a user wants to input
            num_of_classes = request.POST['NumClass']
            num = []
            for i in range(0,int(num_of_classes)):
                num.append(1) # Note that it does not matter what is in the array
                            # it just simply needs to be the size of the number of classes

            # This creates a dict for the template to be able to access num
            context = {'numC': num}

            # Redirect to the schedule making page
            return render(request, 'studentprofile/schedule.html', context)

        # Otherwise 
        else:
            student.name = request.POST['Name']
            student.year = request.POST['Year']
            student.major = request.POST['Major']
            student.num = request.POST['NumClass']
            student.phone = request.POST['phone']
            student.edit = False
            student.save()

            print(student.year, "year")

            if 'save-profile' in request.POST:
                print("HERE")
                return HttpResponseRedirect(reverse('student profile'))
            else:
                num_of_classes = student.num
                num = []
                for i in range(0,int(num_of_classes)):
                    num.append(1) # Note that it does not matter what is in the array
                                # it just simply needs to be the size of the number of classes

                # This creates a dict for the template to be able to access num
                context = {'numC': num}

                # Redirect to the schedule making page
                return render(request, 'studentprofile/schedule.html', context)
    else:
        print("no :( -----------------------------")

def edit_profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse('home'))
    student.edit = True
    print(student)
    student.save()
    return HttpResponseRedirect(reverse('student profile'))

class ProfileView(generic.ListView):
    model = Student
    context_object_name = 'get_majors' # This is the name of the variable within the template
                                       # that holds the list of majors

    template_name = 'studentprofile.html'

    # This function takes the return data and puts it into the context_object_name to be used in the template
    #
    # This is a feature of the generic.ListView
    def get_queryset(self):
        return majors #returns the list containing all the UVa majors

class IndexView(generic.ListView):
    template_name = 'login/index.html'
    context_object_name = 'groups_list'

    def get_queryset(self):
        return StudyGroup.objects.all()


