from django.db.models.signals import m2m_changed, post_save, pre_save
from .models import DicomFile_User, Comment, Patient
from medimageshub.constants import HOST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.dispatch import receiver



# Send email when sharing DICOM file
@receiver(m2m_changed, sender=DicomFile_User)
def access_changed(sender, action, pk_set, instance, **kwargs):
    if action == 'post_add':
        recipient_list = list()
        for pk in pk_set: 
            user = instance.access.get(id=pk)
            recipient_list.append(user.email)

        

        
        params = {'dicom_file': instance, 'host': HOST}
        email_title = f"{instance.owner} shared a DICOM file with you"
        msg_plain = render_to_string('dicoms/emails/dicom_shared.txt', params)
        msg_html = render_to_string('dicoms/emails/dicom_shared.html', params)

        send_mail(
            email_title, 
            msg_plain, 
            "test@medimageshub.com",
            recipient_list,
            html_message=msg_html)


# Send email when comment added on DICOM file you have access to
@receiver(post_save, sender=Comment)
def comment_added(sender, instance, **kwargs):
    recipient_list = set()
    for user in instance.dicom_file.access.all():
        recipient_list.add(user.email)

    recipient_list.add(instance.dicom_file.owner.email)
    recipient_list.remove(instance.author.email)
    has_image = instance.image_url != None


    params = {'comment': instance, 'host': HOST, 'has_image': has_image}
    email_title = f"{instance.author} added a new comment on {instance.dicom_file}"
    msg_plain = render_to_string('dicoms/emails/comment_added.txt', params)
    msg_html = render_to_string('dicoms/emails/comment_added.html', params)

    send_mail(
        email_title, 
        msg_plain, 
        "test@medimageshub.com",
        recipient_list,
        html_message=msg_html)


#Send email to main doctor method
def send_email_to_new_main_doctor(instance, **kwargs):
    #print("SEND EMAIL TO NEW MAIN DOCTOR")
    recipient_list = set()
    recipient_list.add(instance.main_doctor.email)
    params = {'patient': instance, 'host': HOST}
    email_title = f"You are registered as main doctor for {instance}"
    msg_plain = render_to_string('dicoms/emails/main_doctor_changed.txt', params)
    msg_html = render_to_string('dicoms/emails/main_doctor_changed.html', params)
    send_mail(
        email_title, 
        msg_plain, 
        "test@medimageshub.com",
        recipient_list,
        html_message=msg_html
    )


# Send email when comment added on DICOM file you have access to
@receiver(pre_save, sender=Patient)
def main_doctor_changed(sender, instance, **kwargs):
    #print("MAIN DOCTOR CHANGE METHOD")
    current = instance
    if instance.id is None:
        pass
    else:
        previous = Patient.objects.get(pk=instance.id)
        if current.main_doctor.email != previous.main_doctor.email:
            #Sending email to old doctor
            recipient_list = set()
            recipient_list.add(previous.main_doctor.email)
            params = {'patient': current, 'new_doctor': current.main_doctor, 'host': HOST}
            email_title = f"You are no longer registered as main doctor for {current}"
            msg_plain = render_to_string('dicoms/emails/prev_main_doctor_changed.txt', params)
            msg_html = render_to_string('dicoms/emails/prev_main_doctor_changed.html', params)

            send_mail(
                email_title, 
                msg_plain, 
                "test@medimageshub.com",
                recipient_list,
                html_message=msg_html
            )
            send_email_to_new_main_doctor(current)
            

@receiver(post_save, sender=Patient)
def new_patient_added(sender, instance, created, **kwargs):
    #print("NEW PATIENT ADDED METHOD")
    if created:
        send_email_to_new_main_doctor(instance)