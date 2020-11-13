from django.test import TestCase
from django.contrib.auth.models import User
from .models import Student, Schedule, Course, Class
from studygroups.models import StudyGroup, ZoomInfo
from studygroups.views import joinGroup, leaveGroup
import courseInitializer
from .views import make
from mysite.views import submit_profile
from django.test import RequestFactory
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your tests here.

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


class StudentModelCreationTests(TestCase):
    # Boundary case
    def test_profile_is_created_with_default_year(self):
        s1 = Student(name="s1")
        self.assertEqual(s1.year, 1)

    def test_profile_is_created_with_default_major(self):
        s2 = Student(name="s1")
        self.assertEqual(s2.major, "None")

    def test_profile_is_created_with_name(self):
        s3 = Student(name="s1")
        self.assertEqual(s3.name, "s1")

    # Equivalence test
    def test_profile_saved_with_year(self):
        s4 = Student(name="s2Name", year=2, major="Math")
        self.assertEqual(s4.year, 2)

    def test_profile_saved_with_major(self):
        s5 = Student(name="s2Name", year=2, major="Math")
        self.assertEqual(s5.major, "Math")

    def test_profile_saved_with_name(self):
        s6 = Student(name="s2Name", year=2, major="Math")
        self.assertEqual(s6.name, "s2Name")


class StudentModelFunctionTests(TestCase):
    def setUp(self):
        courseInitializer.initializeCourses()  # initialize the courses to add to the schedule
        self.request_factory = RequestFactory()  # This creates a request factor object which is needed when
        # simulating requests

        self.user = User.objects.create_user(
            username='bni3y', email='bni3y@virginia.edu', password='djflksdjldskfjlfdsk')  # Create a simulated user

        self.user1 = User.objects.create_user(
            username='JIM', email='jimbob@virginia.edu', password='jim')  # Create a simulated user

        # Create a Student Object that connects to that user
        self.student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5, phone=1231221234)
        self.student1 = Student(user=self.user, name="Jim")

        # Save the Student Object we have just created
        self.student.save()

        self.schedule = Schedule.objects.create()
        self.list_of_classes_in_sorted_order = []

        cs2150 = Class(course=Course.objects.get(mnemonic="CS", number=2150), schedule=self.schedule, strength=1)
        cs2150.save()
        self.list_of_classes_in_sorted_order.append(cs2150)

        cs3330 = Class(course=Course.objects.get(mnemonic="CS", number=3330), schedule=self.schedule, strength=1)
        cs3330.save()
        self.list_of_classes_in_sorted_order.append(cs3330)

        math1220 = Class(course=Course.objects.get(mnemonic="MATH", number=1220), schedule=self.schedule, strength=2)
        math1220.save()
        self.list_of_classes_in_sorted_order.append(math1220)

        comm2020 = Class(course=Course.objects.get(mnemonic="COMM", number=2020), schedule=self.schedule, strength=3)
        comm2020.save()
        self.list_of_classes_in_sorted_order.append(comm2020)

        econ2010 = Class(course=Course.objects.get(mnemonic="ECON", number=2010), schedule=self.schedule, strength=4)
        econ2010.save()
        self.list_of_classes_in_sorted_order.append(econ2010)
        self.schedule.save()

    def test_get_email(self):
        expected = "bni3y@virginia.edu"
        actual = self.student.get_email()
        self.assertEqual(expected, actual)

    def test_get_classes_in_str_order_not_empty(self):
        self.student.schedule = self.schedule

        expected = self.list_of_classes_in_sorted_order
        actual = self.student.get_classes_in_str_order()

        self.assertEqual(expected, actual)

    def test_get_classes_in_str_order_empty(self):
        expected = []
        actual = self.student.get_classes_in_str_order()

        self.assertEqual(expected, actual)

    def test_get_suggested_groups_none(self):
        expected = []
        actual = self.student.get_suggested_groups()

        self.assertEqual(expected, actual)

    def test_get_suggested_groups_none(self):
        expected = []
        actual = self.student.get_suggested_groups()

        self.assertEqual(expected, actual)

    def test_get_suggested_groups_some(self):
        self.student.schedule = self.schedule

        study_group1 = StudyGroup(name="banana", maxSize=2, course=Course.objects.get(mnemonic="CS", number=2150))
        study_group1.save()

        study_group2 = StudyGroup(name="apple", maxSize=3, course=Course.objects.get(mnemonic="ECON", number=2010))
        study_group2.save()

        expected = [study_group1, study_group2]
        actual = self.student.get_suggested_groups()

        self.assertEqual(expected, actual)

    def test_get_suggested_groups_right_order(self):
        self.student.schedule = self.schedule

        study_group1 = StudyGroup(name="banana", maxSize=2, course=Course.objects.get(mnemonic="CS", number=2150))
        study_group1.save()

        study_group2 = StudyGroup(name="apple", maxSize=3, course=Course.objects.get(mnemonic="CS", number=3330))
        study_group2.save()

        study_group3 = StudyGroup(name="berry", maxSize=2, course=Course.objects.get(mnemonic="MATH", number=1220))
        study_group3.save()

        study_group4 = StudyGroup(name="peach", maxSize=5, course=Course.objects.get(mnemonic="COMM", number=2020))
        study_group4.save()

        study_group5 = StudyGroup(name="kiwi", maxSize=6, course=Course.objects.get(mnemonic="ECON", number=2010))
        study_group5.save()

        expected = [study_group1, study_group2, study_group3]
        actual = self.student.get_suggested_groups()

        self.assertEqual(expected, actual)

    def test_get_available_groups_none(self):
        expected = []
        actual = self.student.get_available_groups()

        self.assertEqual(expected, actual)

    def test_get_available_groups_with_some_same_course(self):
        self.student.schedule = self.schedule

        study_group1 = StudyGroup(name="banana", maxSize=2, course=Course.objects.get(mnemonic="CS", number=2150))
        study_group1.save()

        study_group2 = StudyGroup(name="apple", maxSize=3, course=Course.objects.get(mnemonic="CS", number=3330))
        study_group2.save()

        study_group3 = StudyGroup(name="berry", maxSize=2, course=Course.objects.get(mnemonic="MATH", number=1220))
        study_group3.save()

        study_group4 = StudyGroup(name="peach", maxSize=5, course=Course.objects.get(mnemonic="COMM", number=2020))
        study_group4.save()

        study_group5 = StudyGroup(name="kiwi", maxSize=6, course=Course.objects.get(mnemonic="ECON", number=2010))
        study_group5.save()

        expected = [study_group4, study_group5]
        actual = self.student.get_available_groups()

        self.assertEqual(expected, actual)

    def test_get_available_groups_with_none_in_same_course(self):
        self.student.schedule = self.schedule

        study_group1 = StudyGroup(name="banana", maxSize=2, course=Course.objects.get(mnemonic="CS", number=2102))
        study_group1.save()

        study_group2 = StudyGroup(name="apple", maxSize=3, course=Course.objects.get(mnemonic="CS", number=4102))
        study_group2.save()

        expected = []
        actual = self.student.get_available_groups()

        self.assertEqual(expected, actual)


class ScheduleModelCreationTests(TestCase):
    # This is run before every test in this class
    def setUp(self):
        courseInitializer.initializeCourses()  # initialize the courses to add to the schedule

    # This tests the get_classes() function inside the schedule when the schedule is empty
    def test_empty_schedule_returns_empty_list_of_classes(self):
        schedule = Schedule.objects.create()
        schedule.save()

        actual = schedule.get_classes()
        expected = []
        self.assertListEqual(expected, actual)

    def test_invalid_class(self):
        schedule = Schedule.objects.create()
        try:
            invalid_course = Class(course=Course.objects.get(mnemonic="CS", number=3241), schedule=schedule, strength=1)
        except:
            self.assertRaises(Course.DoesNotExist)

    def test_full_schedule_returns_correct_list_of_classes(self):
        schedule = Schedule.objects.create()

        expected = []
        cs2150 = Class(course=Course.objects.get(mnemonic="CS", number=2150), schedule=schedule, strength=1)
        cs2150.save()
        expected.append(cs2150)

        cs3330 = Class(course=Course.objects.get(mnemonic="CS", number=3330), schedule=schedule, strength=1)
        cs3330.save()
        expected.append(cs3330)

        math1220 = Class(course=Course.objects.get(mnemonic="MATH", number=1220), schedule=schedule, strength=2)
        math1220.save()
        expected.append(math1220)

        comm2020 = Class(course=Course.objects.get(mnemonic="COMM", number=2020), schedule=schedule, strength=3)
        comm2020.save()
        expected.append(comm2020)

        econ2010 = Class(course=Course.objects.get(mnemonic="ECON", number=2010), schedule=schedule, strength=4)
        econ2010.save()
        expected.append(econ2010)

        schedule.save()
        actual = schedule.get_classes()
        self.assertListEqual(expected, actual)


class SubmitProfileTest(TestCase):
    # This sets up all our tests so that they can access these fields directly
    def setUp(self):
        self.request_factory = RequestFactory()  # This creates a request factor object which is needed when
        # simulating requests

        self.user = User.objects.create_user(
            username='bni3y', email='bni3y@virginia.edu', password='jasdflkjsdfalk;f')  # Create a simulated user

    # Test that when user presses the generate schedule button when first creating profile that it redirects
    # to correct page
    #
    # Note that there is not student object associated with the user
    def test_submit_profile_first_time_valid(self):
        request = self.request_factory.post(reverse('submit'),
                                            {'Name': ['Jim'],
                                             'Year': ['2021'],
                                             'Major': ['Systems Engineering'],
                                             'NumClass': ['2'],
                                             'phone': ['6451827384'],
                                             'generate-schedule': ['']})  # Generate Schedule
        request.user = self.user
        actual = len(submit_profile(request).content)

        num = [1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {'numC': num}).content)

        self.assertEqual(actual, expected)

    # Test error message when name field is blank when creating profile for first time
    #
    # Note that there is not student object associated with the user
    def test_submit_profile_first_time_no_name(self):
        request = self.request_factory.post(reverse('submit'),
                                            {'Name': [''],
                                             'Year': ['2021'],
                                             'Major': ['Systems Engineering'],
                                             'NumClass': ['2'],
                                             'phone': ['6451827384'],
                                             'generate-schedule': ['']})
        request.user = self.user
        actual = len(submit_profile(request).content)

        num = [1, 1]

        expected = len(render(request, 'studentprofile.html', {
            'error_message': "Username cannot be blank.",
            'get_majors': majors,
        }).content)

        self.assertEqual(actual, expected)

    # Test that when user presses the save button after editing profile it redirects to correct page
    def test_submit_profile_edit_save_valid(self):
        request = self.request_factory.post(reverse('submit'),
                                            {'Name': ['Jim'],
                                             'Year': ['2021'],
                                             'Major': ['Systems Engineering'],
                                             'NumClass': ['2'],
                                             'phone': ['6451827384'],
                                             'save-profile': ['']})
        request.user = self.user
        # Create a Student Object so that it is an existing user
        student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5, phone=8172229876)
        student.save()

        actual = len(submit_profile(request).content)
        print(submit_profile(request))

        num = [1, 1]
        expected = len(HttpResponseRedirect(reverse('student profile')).content)

        self.assertEqual(actual, expected)

    # Test that when user presses the edit schedule button after editing profile it redirects to correct page
    def test_submit_profile_edit_schedule_valid(self):
        request = self.request_factory.post(reverse('submit'),
                                            {'Name': ['Jim'],
                                             'Year': ['2021'],
                                             'Major': ['Systems Engineering'],
                                             'NumClass': ['2'],
                                             'phone': ['6451827384'],
                                             'generate-schedule': ['']})  # Indicates edit schedule was pressed
        request.user = self.user
        # Create a Student Object so that it is an existing user
        student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5, phone=8172229876)
        student.save()

        actual = len(submit_profile(request).content)
        print(submit_profile(request))

        num = [1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {'numC': num}).content)

        self.assertEqual(actual, expected)

    # Test error message when name field is blank when editing existing student profile
    def test_submit_profile_edit_no_name(self):
        request = self.request_factory.post(reverse('submit'),
                                            {'Name': [''],
                                             'Year': ['2021'],
                                             'Major': ['Systems Engineering'],
                                             'NumClass': ['2'],
                                             'phone': ['6451827384'],
                                             'save-profile': ['']})
        request.user = self.user
        # Create a Student Object so that it is an existing user
        student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5, phone=8172229876)
        student.save()

        actual = len(submit_profile(request).content)

        expected = len(render(request, 'studentprofile.html', {
            'error_message': "Username cannot be blank.",
            'get_majors': majors
        }).content)

        self.assertEqual(actual, expected)


class MakeTest(TestCase):
    # This sets up all our tests so that they can access these fields directly
    def setUp(self):
        courseInitializer.initializeCourses()  # initialize the courses to add to the schedule

        self.request_factory = RequestFactory()  # This creates a request factor object which is needed when
        # simulating requests

        self.user = User.objects.create_user(
            username='bni3y', email='bni3y@virginia.edu', password='djflksdjldskfjlfdsk')  # Create a simulated user

        # Create a Student Object that connects to that user
        student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5, phone=1231221234)

        # Save the Student Object we have just created
        student.save()

    # Test when make is valid
    def test_make_valid(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            # Note that we do not need a CSRF malware token
                                            # when simulating tests
                                            {'class1': ['CS 3330'], 'strength1': ['1'],
                                             'class2': ['CS 1110'], 'strength2': ['2'],
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['2'],
                                             'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content)  # Since directly comparing the objects doesn't work
        # comparing the lengths of their content will
        # especially for error messages

        expected = len(HttpResponseRedirect(reverse('student profile')).content)

        self.assertEqual(expected, actual)

    # Test error message when there is one or more strengths not in range
    def test_make_strength_not_in_range(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': ['CS 3330'], 'strength1': ['1'],
                                             'class2': ['CS 1110'], 'strength2': ['2'],
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['2'],
                                             'class5': ['ECON 2020'], 'strength5': ['0']})  # 0 is not in range 0 - 5

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "Strength must be a digit between 1 and 5.",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when there is one or more strengths are blank
    def test_make_missing_strength(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': ['CS 3330'], 'strength1': ['1'],
                                             'class2': ['CS 1110'], 'strength2': ['2'],
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['2'],
                                             'class5': ['ECON 2020'], 'strength5': ['']})  # This strength is blank

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "You are missing some required strength fields.",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when there is one or more strengths are not a digit
    def test_make_strength_not_digit(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': ['CS 3330'], 'strength1': ['1'],
                                             'class2': ['CS 1110'], 'strength2': ['d'],  # d is not a digit
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['b'],
                                             'class5': ['ECON 2020'], 'strength5': ['a']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "Strength must be a digit.",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when there are not enough classes inputted
    def test_make_not_enough_classes(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': [''], 'strength1': ['1'],  # Missing class
                                             'class2': ['CS 1110'], 'strength2': ['3'],
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['2'],
                                             'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "You are missing some required course fields.",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when one or more class inputted is not formatted correctly
    def test_make_class_not_formatted_correctly(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': ['CS3330'], 'strength1': ['1'],
                                             # Should have a space between CS and 3330
                                             'class2': ['CS 1110'], 'strength2': ['3'],
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['2'],
                                             'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "Class must be a course mnemonic (i.e. CS) followed by a space followed by a 4 digit number (i.e. 3240).",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when one or more class inputted does not have a number that is long enough
    def test_make_class_number_not_long_enough(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': ['CS 333'], 'strength1': ['1'],  # Only 3 digits for CS 333
                                             'class2': ['CS 1110'], 'strength2': ['3'],
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['2'],
                                             'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "Class number must be 4 digits.",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when one or more class inputted does not have a digit when it should
    def test_make_class_number_not_a_digit(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': ['CS 3330'], 'strength1': ['1'],
                                             'class2': ['CS AAAA'], 'strength2': ['3'],  # AAAA should be digits
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['2'],
                                             'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "Class number must be a digit.",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when one or more class inputted does not exist
    def test_make_class_does_not_exist(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': ['CS 3330'], 'strength1': ['1'],
                                             'class2': ['CS 3241'], 'strength2': ['3'],  # CS 3241 is not a valid class
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['2'],
                                             'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "One or more courses inputted does not exist.",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when a class is entered multiple times
    def test_make_class_Entered_multiple_times(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': ['CS 3330'], 'strength1': ['1'],
                                             'class2': ['CS 3330'], 'strength2': ['3'],
                                             # CS 3330 is a repeat entry of class1
                                             'class3': ['CS 3240'], 'strength3': ['1'],
                                             'class4': ['CS 2150'], 'strength4': ['2'],
                                             'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "One or more classes entered multiple times. Each course field should be unique.",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test Student Object with null schedule
    def test_null_schedule(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
                                            {'class1': [''], 'strength1': [''],
                                             'class2': [''], 'strength2': [''],
                                             'class3': [''], 'strength3': [''],
                                             'class4': [''], 'strength4': [''],
                                             'class5': [''], 'strength5': ['']})  # no class entered

        request.user = self.user
        actual = len(make(request).content)

        numC = [1, 1, 1, 1, 1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "Entering one or more classes to complete your schedule.",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)


class StudyGroupModelFunctionTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()  # This creates a request factor object which is needed when
        # simulating requests

        self.user = User.objects.create_user(
            username='bni3y', email='bni3y@virginia.edu', password='djflksdjldskfjlfdsk')  # Create a simulated user

        # Create a Student Object that connects to that user
        self.student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5, phone=1231221234)

        # Different Users and Students
        self.user1 = User.objects.create_user(
            username='jim1', email='jim@virginia.edu', password='ffff')  # Create a simulated user
        self.student1 = Student(user=self.user1, name="Jim", year=3, major="Computer Science", num=5, phone=1231221234)

        self.user2 = User.objects.create_user(
            username='jim2', email='jim2@virginia.edu', password='dddd')  # Create a simulated user
        self.student2 = Student(user=self.user2, name="Jim2", year=2, major="Computer Science", num=5, phone=1231221234)

        # Save the Student Object we have just created
        self.student.save()
        self.student1.save()
        self.student2.save()

    def test_get_members_empty(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        actual = study_group.get_members()
        expected = []

        self.assertEqual(expected, actual)

    def test_get_members_not_empty(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        # Add Student to group
        study_group.members.add(self.student)
        study_group.save()

        actual = study_group.get_members()
        expected = [self.student]

        self.assertEqual(expected, actual)

    def test_get_members_email_empty(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        actual = study_group.get_members_email()
        expected = ''

        self.assertEqual(expected, actual)

    def test_get_members_email_not_empty(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        # Add Students to group
        study_group.members.add(self.student1)
        study_group.save()
        study_group.members.add(self.student2)
        study_group.save()

        actual = study_group.get_members_email()
        expected = 'Jim (jim@virginia.edu), Jim2 (jim2@virginia.edu)'

        self.assertEqual(expected, actual)

    def test_get_members_string_empty(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        actual = study_group.get_members_string()
        expected = ''

        self.assertEqual(expected, actual)

    def test_get_members_string_not_empty(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        # Add Students to group
        study_group.members.add(self.student1)
        study_group.save()
        study_group.members.add(self.student2)
        study_group.save()

        actual = study_group.get_members_string()
        expected = 'Jim, Jim2'

        self.assertEqual(expected, actual)


class JoinGroupTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()  # This creates a request factor object which is needed when
        # simulating requests

        self.user = User.objects.create_user(
            username='bni3y', email='bni3y@virginia.edu', password='djflksdjldskfjlfdsk')  # Create a simulated user

        # Create a Student Object that connects to that user
        self.student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5, phone=1231221234)

        # Different Users and Students
        self.user1 = User.objects.create_user(
            username='jim1', email='jim@virginia.edu', password='ffff')  # Create a simulated user
        self.student1 = Student(user=self.user1, name="Jim", year=3, major="Computer Science", num=5, phone=1231221234)

        self.user2 = User.objects.create_user(
            username='jim2', email='jim2@virginia.edu', password='dddd')  # Create a simulated user
        self.student2 = Student(user=self.user2, name="Jim2", year=2, major="Computer Science", num=5, phone=1231221234)

        # Save the Student Object we have just created
        self.student.save()
        self.student1.save()
        self.student2.save()

    def test_student_already_in_group(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        # Add Student to group
        study_group.members.add(self.student)
        study_group.save()

        # Obtain Group ID to pass as a parameter to the request
        group = StudyGroup.objects.get(name="banana")
        id = group.id

        # Make request and call joinGroup
        request = self.request_factory.post(reverse('studygroups:joinGroup'), {
            'Group': [str(id)], 'edit': ['']})
        request.user = self.user
        joinGroup(request)

        actual = study_group.get_members()
        expected = [self.student]

        self.assertEqual(expected, actual)

    def test_student_not_in_group(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        # Obtain Group ID to pass as a parameter to the request
        group = StudyGroup.objects.get(name="banana")
        id = group.id

        # Make request and call joinGroup
        request = self.request_factory.post(reverse('studygroups:joinGroup'), {
            'Group': [str(id)], 'edit': ['']})
        request.user = self.user
        joinGroup(request)

        actual = study_group.get_members()
        expected = [self.student]

        self.assertEqual(expected, actual)

    def test_join_full_group(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=2, )
        study_group.save()

        # Add Students to group
        study_group.members.add(self.student1)
        study_group.save()
        study_group.members.add(self.student2)
        study_group.save()

        # Obtain Group ID to pass as a parameter to the request
        group = StudyGroup.objects.get(name="banana")
        id = group.id

        # Make request and call joinGroup
        request = self.request_factory.post(reverse('studygroups:joinGroup'), {
            'Group': [str(id)], 'edit': ['']})
        request.user = self.user
        joinGroup(request)

        actual = study_group.get_members()
        expected = [self.student1, self.student2]

        self.assertEqual(expected, actual)

    def test_join_group_does_not_exist(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=2, )
        study_group.save()

        # Add Students to group
        study_group.members.add(self.student1)
        study_group.save()
        study_group.members.add(self.student2)
        study_group.save()

        # Obtain Group ID to pass as a parameter to the request
        group = StudyGroup.objects.get(name="banana")
        id = group.id

        # Delete the group
        group.delete()

        # Make request and call joinGroup
        request = self.request_factory.post(reverse('studygroups:joinGroup'), {
            'Group': [str(id)], 'edit': ['']})
        request.user = self.user

        # This should fail and thus yield a StudyGroup.DoesNotExist Exception
        self.assertRaises(StudyGroup.DoesNotExist, joinGroup, request=request)


class LeaveGroupTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()  # This creates a request factor object which is needed when
        # simulating requests

        self.user = User.objects.create_user(
            username='bni3y', email='bni3y@virginia.edu', password='djflksdjldskfjlfdsk')  # Create a simulated user

        # Create a Student Object that connects to that user
        self.student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5, phone=1231221234)

        # Different Users and Students
        self.user1 = User.objects.create_user(
            username='jim1', email='jim@virginia.edu', password='ffff')  # Create a simulated user
        self.student1 = Student(user=self.user1, name="Jim", year=3, major="Computer Science", num=5, phone=1231221234)

        self.user2 = User.objects.create_user(
            username='jim2', email='jim2@virginia.edu', password='dddd')  # Create a simulated user
        self.student2 = Student(user=self.user2, name="Jim2", year=2, major="Computer Science", num=5, phone=1231221234)

        # Save the Student Object we have just created
        self.student.save()
        self.student1.save()
        self.student2.save()

    def test_leave_group_student_no_delete(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        # Add Student to group
        study_group.members.add(self.student)
        study_group.save()
        study_group.members.add(self.student1)
        study_group.save()

        # Obtain Group ID to pass as a parameter to the request
        group = StudyGroup.objects.get(name="banana")
        id = group.id

        # Make request and call leaveGroup
        request = self.request_factory.post(reverse('studygroups:leaveGroup'), {
            'Group': [str(id)], 'edit': ['']})
        request.user = self.user
        leaveGroup(request)

        actual = study_group.get_members()
        expected = [self.student1]

        self.assertEqual(expected, actual)

    def test_leave_group_student_yes_delete(self):
        # Make a study group
        zoom = ZoomInfo(group_id = "1112")
        zoom.save()
        study_group = StudyGroup(name="banana", maxSize=4, zoom = zoom)
        study_group.save()

        # Add Student to group
        self.student.group_id = "1112"
        study_group.members.add(self.student)
        study_group.save()

        # Obtain Group ID to pass as a parameter to the request
        group = StudyGroup.objects.get(name="banana")
        id = group.id

        # Make request and call leaveGroup
        request = self.request_factory.post(reverse('studygroups:leaveGroup'), {
            'Group': [str(id)], 'edit': ['']})
        request.user = self.user
        leaveGroup(request)

        # Try to access group again
        self.assertRaises(StudyGroup.DoesNotExist, StudyGroup.objects.get, name="banana")

    def test_leave_group_student_not_in_group(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=4, )
        study_group.save()

        # Add Student to group
        study_group.members.add(self.student1)
        study_group.save()

        # Obtain Group ID to pass as a parameter to the request
        group = StudyGroup.objects.get(name="banana")
        id = group.id

        # Make request and call leaveGroup
        request = self.request_factory.post(reverse('studygroups:leaveGroup'), {
            'Group': [str(id)], 'edit': ['']})
        request.user = self.user
        leaveGroup(request)

        actual = study_group.get_members()
        expected = [self.student1]
        self.assertEqual(expected, actual)

    def test_leave_group_does_not_exist(self):
        # Make a study group
        study_group = StudyGroup(name="banana", maxSize=2, )
        study_group.save()

        # Add Students to group
        study_group.members.add(self.student1)
        study_group.save()
        study_group.members.add(self.student2)
        study_group.save()

        # Obtain Group ID to pass as a parameter to the request
        group = StudyGroup.objects.get(name="banana")
        id = group.id

        # Delete the group
        group.delete()

        # Make request and call leaveGroup
        request = self.request_factory.post(reverse('studygroups:leaveGroup'), {
            'Group': [str(id)], 'edit': ['']})
        request.user = self.user

        # This should fail and thus yield a StudyGroup.DoesNotExist Exception
        self.assertRaises(StudyGroup.DoesNotExist, leaveGroup, request=request)