from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from .models import Channel, Thread, Comment
from .forms import ChannelForm, ThreadForm, CommentForm

# Create your views here.
class ChannelView(generic.ListView):
    model = Channel
    template_name = 'forumapp/channel.html'

    form_class = ChannelForm
    initial = {'key': 'value'}

    queryset = Channel.objects.all()
    context_object_name = 'channel_list'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, self.context_object_name: self.queryset})
   
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            channel_name = form.cleaned_data['channel_name']
            owner = request.user
            pub_date = timezone.now()

            channel = Channel(channel_name=channel_name, owner=owner, pub_date=pub_date)
            channel.save()

            return HttpResponseRedirect(reverse('forumapp:thread', kwargs={'channel': channel_name}))
        else:
            return Http404("Invalid form submission")

class ThreadView(generic.DetailView):
    model = Thread
    template_name = 'forumapp/thread.html'

    form_class = ThreadForm
    initial = {'key': 'value'}

    queryset = Thread.objects.all()
    context_object_name = 'thread_list'

    # Return querylist of threads in the given channel
    def get_object(self):
        c_name = self.kwargs.get('channel')
        
        return Thread.objects.filter(channel__channel_name=c_name)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, self.context_object_name: self.queryset})
   
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            channel = Channel.objects.get(channel_name=kwargs.get('channel'))
            thread_name = form.cleaned_data['thread_name']
            description = form.cleaned_data['description']
            owner = request.user
            pub_date = timezone.now()

            thread = Thread(channel=channel, thread_name=thread_name, description=description, owner=owner, pub_date=pub_date)
            thread.save()

            return HttpResponseRedirect(reverse('forumapp:comment', kwargs={'channel': thread.channel.channel_name, 'thread': thread.thread_id}))
        else:
            return Http404("Invalid form submission")

class CommentView(generic.DetailView):
    model = Comment
    template_name = 'forumapp/comment.html'

    form_class = CommentForm
    initial = {'key': 'value'}

    queryset = Comment.objects.all()
    context_object_name = 'comment_list'

    # Return querylist of comments in the given channel and thread
    def get_object(self):
        t_id = self.kwargs.get('thread')
        c_name = self.kwargs.get('channel')

        return Comment.objects.filter(thread__thread_id=t_id, thread__channel__channel_name=c_name)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, self.context_object_name: self.get_object()})
   
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            thread = Thread.objects.get(channel__channel_name=kwargs.get('channel'), thread_id=kwargs.get('thread'))
            text = form.cleaned_data['text']
            owner = request.user
            pub_date = timezone.now()

            comment = Comment(thread=thread, text=text, owner=owner, pub_date=pub_date)
            comment.save()

            return HttpResponseRedirect(reverse('forumapp:comment', kwargs={'channel': thread.channel.channel_name, 'thread': thread.thread_id}))
        else:
            return CommentView.get(self, request, *args, **kwargs)
