from __future__ import absolute_import
import os
from django.conf import settings
from django import template
from django.core.mail import send_mail, EmailMultiAlternatives
from yell import Notification



class EmailBackend(Notification):
    """
    Send emails via :attr:`django.core.mail.send_mail`
    """

    subject = None
    """ Email subject """
    body = None
    """ Email body """
    

    def get_subject(self, *args, **kwargs):
        """
        Return a subject. Override if you need templating or such. 
        """
        return self.subject
    
    def get_body(self, *args, **kwargs):
        """
        Return a body. Override if you need templating or such.
        """
        return self.body
    
    def get_from(self, *args, **kwargs):
        return settings.DEFAULT_FROM_EMAIL

    def get_to(self, *args, **kwargs):
        return kwargs.get('to')
    
    def notify(self, *args, **kwargs):
        
        return send_mail(
            self.get_subject(*args, **kwargs),
            self.get_body(*args, **kwargs),
            self.get_from(*args, **kwargs),
            self.get_to(*args, **kwargs),
        )

class MultipartEmailBackend(EmailBackend):
    """
    Send emails via :class:`django.core.mail.EmailMultiAlternatives`
    """
    default_content_type = 'text/plain'
    """
    The default content type. 
    """
    
    body = {}
    """
    Email body mapping content type to message. Requires at least a key for 
    :attr:`default_content_type`.
    """

    
    def get_body(self, *args, **kwargs):
        assert self.default_content_type in self.body, "No message body for default content type '%s'" % self.default_content_type
        return self.body
    
    def get_default_body(self, *args, **kwargs):
        return self.get_body(*args, **kwargs)[self.default_content_type]
    
    def notify(self, *args, **kwargs):        
        message = EmailMultiAlternatives(
            self.get_subject(*args, **kwargs),
            self.get_default_body(*args, **kwargs),
            self.get_from(*args, **kwargs),
            self.get_to(*args, **kwargs)
        )
        
        for content_type, body in self.get_body(*args, **kwargs).iteritems():
            if content_type == self.default_content_type: continue
            message.attach_alternative(body, content_type)
        
        return message.send()
        
class TemplatedEmailBackend(MultipartEmailBackend):
    """
    Generates email bodies from templates.
    
    :example:
    
    ::
    
        class SignupMessage(TemplatedEmailBackend):
            name = 'signup'
            subject = "Welcome to %s" % Site.objects.get_current().name
            content_types = ['text/plain', 'text/html']
        
    The `SignupMessage` class would look up following templates for the email body:
    
    * `yell/signup.txt`
    * `yell/signup.html`
    
    """
    content_types = (
        ('text/plain', '.txt'),
        ('text/html', '.html')
    )
    """
    Default content types to render
    """
        
    # Memoize
    _body = None
    
    def get_path(self, name, ext):
        """
        Get the path to a given template name. Override if you wish to
        store your templates in a custom folder outside of `yell/`.
        """
        return os.path.join('yell', '{0}{1}'.format(name, ext))

    def get_body(self, *args, **kwargs):
        """ 
        Render message bodies by using all the content types defined
        in :attr:`content_types`
        """
        if self._body is None:
            self._body = {}
            for ctype, ext in self.content_types:
                tpl = template.loader.get_template(self.get_path(self.name, ext))
                self._body[ctype] = tpl.render(template.Context(kwargs))
        return self._body
    
