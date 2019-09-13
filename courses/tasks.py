from .models import EnrolledModules, Modules
import datetime


def set_current_module(module, enrolled, days=7):
    # todo make this function asynchronous

    # disable access
    modules = EnrolledModules.objects.filter(enrolled_id=enrolled.id).all()

    for mod in modules:
        # todo call function to revoke access
        pass

    # check if module already exists for the enrollment
    check = EnrolledModules.objects.filter(enrolled_id=enrolled.id, module_id=module.id).first()

    if not check:
        check = EnrolledModules.objects.create(user=enrolled.user, module=module, enrolled=enrolled, days=days)

    # todo grant access to specific module

    check.date_activated = datetime.datetime.now()
    check.set_expires()
    check.save()

    # update enrolled
    enrolled.current_module = module.id
    enrolled.save()

    # send notification email
    enrolled.user.email_user(subject="You have been granted access to {}".format(module.name),
                             subtitle="Dear {},".format(enrolled.user.first_name),
                             title="You have been granted access to {}".format(module.name), button_value="#",
                             button_link="View Module Content",
                             content="Congratulations! You have been granted access to the module, {}, of the {} "
                                     "course. Please follow the link below to get started".format(module.name,
                                                                                                  enrolled.course.name))