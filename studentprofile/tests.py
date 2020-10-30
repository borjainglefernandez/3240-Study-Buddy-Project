
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Student, Schedule, Course, Class
import courseInitializer
from .views import make
from mysite.views import submit_profile
from django.test import RequestFactory
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


# Create your tests here. 
class StudentModelCreationTests(TestCase):
    # Boundary case
    def test_profile_is_created_with_default_year(self):
        s1 = Student(name="s1")
        self.assertEqual(s1.year,1)
       
    def test_profile_is_created_with_default_major(self):
        s2 = Student(name="s1")
        self.assertEqual(s2.major,"None")
    
    def test_profile_is_created_with_name(self):
        s3 = Student(name="s1")
        self.assertEqual(s3.name,"s1")

    #Equivalence test
    def test_profile_saved_with_year(self):
        s4 = Student(name="s2Name",year=2,major="Math")
        self.assertEqual(s4.year,2)

    def test_profile_saved_with_major(self):
        s5 = Student(name="s2Name",year=2,major="Math")
        self.assertEqual(s5.major,"Math")

    def test_profile_saved_with_name(self):
        s6 = Student(name="s2Name",year=2,major ="Math")
        self.assertEqual(s6.name,"s2Name")

class ScheduleModelCreationTests(TestCase):
    # This is run before every test in this class
    def setUp(self):
        courseInitializer.initializeCourses() # initialize the courses to add to the schedule

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
        cs2150 = Class(course = Course.objects.get(mnemonic = "CS", number = 2150), schedule = schedule, strength = 1)
        cs2150.save()
        expected.append(cs2150)

        cs3330 = Class(course = Course.objects.get(mnemonic = "CS", number = 3330), schedule = schedule, strength = 1)
        cs3330.save()
        expected.append(cs3330)

        math1220 = Class(course = Course.objects.get(mnemonic = "MATH", number = 1220), schedule = schedule, strength = 2)
        math1220.save()
        expected.append(math1220)

        comm2020 = Class(course = Course.objects.get(mnemonic = "COMM", number = 2020), schedule = schedule, strength = 3)
        comm2020.save()
        expected.append(comm2020)

        econ2010 = Class(course = Course.objects.get(mnemonic = "ECON", number = 2010), schedule = schedule, strength = 4)
        econ2010.save()
        expected.append(econ2010)


        schedule.save()
        actual = schedule.get_classes()
        self.assertListEqual(expected, actual)

class SubmitProfileTest(TestCase):
    # This sets up all our tests so that they can access these fields directly
    def setUp(self):
        self.request_factory = RequestFactory() # This creates a request factor object which is needed when
                                                # simulating requests

        self.user = User.objects.create_user(
        username='bni3y', email='bni3y@virginia.edu', password='jasdflkjsdfalk;f') # Create a simulated user

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
                                             'generate-schedule': ['']}) # Generate Schedule
        request.user = self.user
        actual = len(submit_profile(request).content)

        num = [1,1]
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
                                             'generate-schedule': ['']})
        request.user = self.user
        actual = len(submit_profile(request).content)

        num = [1,1]
        expected = len(render(request, 'studentprofile.html', {
        'error_message': "Username cannot be blank.",
        }).content)

        self.assertEqual(actual, expected)

    # Test that when user presses the save button after editing profile it redirects to correct page
    def test_submit_profile_edit_save_valid(self):
        request = self.request_factory.post(reverse('submit'),
                                            {'Name': ['Jim'],
                                             'Year': ['2021'],
                                             'Major': ['Systems Engineering'],
                                             'NumClass': ['2'],
                                             'save-profile': ['']})
        request.user = self.user
        # Create a Student Object so that it is an existing user
        student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5)
        student.save()

        actual = len(submit_profile(request).content)
        print(submit_profile(request))

        num = [1,1]
        expected = len(HttpResponseRedirect(reverse('student profile')).content)

        self.assertEqual(actual, expected)

    # Test that when user presses the edit schedule button after editing profile it redirects to correct page
    def test_submit_profile_edit_schedule_valid(self):
        request = self.request_factory.post(reverse('submit'),
                                            {'Name': ['Jim'],
                                             'Year': ['2021'],
                                             'Major': ['Systems Engineering'],
                                             'NumClass': ['2'],
                                             'generate-schedule': ['']}) # Indicates edit schedule was pressed
        request.user = self.user
        # Create a Student Object so that it is an existing user
        student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5)
        student.save()

        actual = len(submit_profile(request).content)
        print(submit_profile(request))

        num = [1,1]
        expected = len(render(request, 'studentprofile/schedule.html', {'numC': num}).content)

        self.assertEqual(actual, expected)

    # Test error message when name field is blank when editing existing student profile
    def test_submit_profile_edit_no_name(self):
        request = self.request_factory.post(reverse('submit'),
                                            {'Name': [''], # No name field
                                             'Year': ['2021'],
                                             'Major': ['Systems Engineering'],
                                             'NumClass': ['2'],
                                             'generate-schedule': ['']})
        request.user = self.user

        # Create a Student Object so that it is an existing user
        student = Student(user=self.user, name="Borja", year=1, major="Computer Science", num=5)
        student.save()

        actual = len(submit_profile(request).content)

        expected = len(render(request, 'studentprofile.html', {
        'error_message': "Username cannot be blank.",
        }).content)

        self.assertEqual(actual, expected)


class MakeTest(TestCase):
    # This sets up all our tests so that they can access these fields directly
    def setUp(self):
        courseInitializer.initializeCourses() # initialize the courses to add to the schedule

        self.request_factory = RequestFactory() # This creates a request factor object which is needed when
                                                # simulating requests

        self.user = User.objects.create_user(
        username='bni3y', email='bni3y@virginia.edu', password='djflksdjldskfjlfdsk') # Create a simulated user

        # Create a Student Object that connects to that user
        student = Student(user = self.user, name = "Borja", year = 1, major = "Computer Science", num = 5)

        # Save the Student Object we have just created
        student.save()

    # Test when make is valid
    def test_make_valid(self):

        request = self.request_factory.post(reverse('studentprofile:generateSchedule'), # Note that we do not need a CSRF malware token
                                                                                        # when simulating tests
        {'class1': ['CS 3330'], 'strength1': ['1'],
         'class2': ['CS 1110'], 'strength2': ['2'],
         'class3': ['CS 3240'], 'strength3': ['1'],
         'class4': ['CS 2150'], 'strength4': ['2'],
         'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content) # Since directly comparing the objects doesn't work
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
         'class5': ['ECON 2020'], 'strength5': ['0']}) # 0 is not in range 0 - 5

        request.user = self.user
        actual = len(make(request).content)

        numC = [1,1,1,1,1]
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
         'class5': ['ECON 2020'], 'strength5': ['']}) # This strength is blank

        request.user = self.user
        actual = len(make(request).content)

        numC = [1,1,1,1,1]
        expected = len(render(request, 'studentprofile/schedule.html', {
        'error_message': "You are missing some required strength fields.",
        'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when there is one or more strengths are not a digit
    def test_make_strength_not_digit(self):

        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
        {'class1': ['CS 3330'], 'strength1': ['1'],
         'class2': ['CS 1110'], 'strength2': ['d'], # d is not a digit
         'class3': ['CS 3240'], 'strength3': ['1'],
         'class4': ['CS 2150'], 'strength4': ['b'],
         'class5': ['ECON 2020'], 'strength5': ['a']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1,1,1,1,1]
        expected = len(render(request, 'studentprofile/schedule.html', {
        'error_message': "Strength must be a digit.",
        'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when there are not enough classes inputted
    def test_make_not_enough_classes(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
        {'class1': [''], 'strength1': ['1'], # Missing class
         'class2': ['CS 1110'], 'strength2': ['3'],
         'class3': ['CS 3240'], 'strength3': ['1'],
         'class4': ['CS 2150'], 'strength4': ['2'],
         'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1,1,1,1,1]
        expected = len(render(request, 'studentprofile/schedule.html', {
        'error_message': "You are missing some required course fields.",
        'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when one or more class inputted is not formatted correctly
    def test_make_class_not_formatted_correctly(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
        {'class1': ['CS3330'], 'strength1': ['1'], # Should have a space between CS and 3330
         'class2': ['CS 1110'], 'strength2': ['3'],
         'class3': ['CS 3240'], 'strength3': ['1'],
         'class4': ['CS 2150'], 'strength4': ['2'],
         'class5': ['ECON 2020'], 'strength5': ['1']})

        request.user = self.user
        actual = len(make(request).content)

        numC = [1,1,1,1,1]
        expected = len(render(request, 'studentprofile/schedule.html', {
            'error_message': "Class must be a course mnemonic (i.e. CS) followed by a space followed by a 4 digit number (i.e. 3240).",
            'numC': numC
        }).content)

        self.assertEqual(expected, actual)

    # Test error message when one or more class inputted does not have a number that is long enough
    def test_make_class_number_not_long_enough(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
        {'class1': ['CS 333'], 'strength1': ['1'], # Only 3 digits for CS 333
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
         'class2': ['CS AAAA'], 'strength2': ['3'], # AAAA should be digits
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
         'class2': ['CS 3241'], 'strength2': ['3'], # CS 3241 is not a valid class
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
         'class2': ['CS 3330'], 'strength2': ['3'], # CS 3330 is a repeat entry of class1
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
        
    # Test for Student object with null schedule 
    def test_null_schedule(self):
        request = self.request_factory.post(reverse('studentprofile:generateSchedule'),
        {'class1': [''], 'strength1': [''],
         'class2': [''], 'strength2': [''], 
         'class3': [''], 'strength3': [''],
         'class4': [''], 'strength4': [''],
         'class5': [''], 'strength5': ['']}) # no class entered

        request.user = self.user
        actual = len(make(request).content)

        numC = [1,1,1,1,1]
        expected = len(render(request, 'studentprofile/schedule.html', {
        'error_message': "Entering one or more classes to complete your profile.",
        'numC': numC
        }).content)

        self.assertEqual(expected, actual)

