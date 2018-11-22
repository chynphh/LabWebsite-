from django.dispatch import Signal
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from notifications.signals import notify
from django.db.models.signals import post_save

from bbs.models import Post, Reply, Comment, MyUser
from bbs.email import send_text_email



@receiver(post_save, sender=Comment, dispatch_uid="comment_post_save")
def send_comment_message(sender, **kwargs):
    comment = kwargs['instance']

    recipient = comment.user_to
    verb = f'you get a comment from {comment.user.name}'
    message = {}
    message['recipient'] = recipient            # 消息接收人
    message['verb'] = verb                      # 消息标题
    message['description'] = comment.content    # 评论详细内容
    message['target'] = comment.reply.post      # 目标对象
    message['action_object'] = comment.reply    # 评论记录
    notify.send(comment.user, **message)
    if recipient.mailnotify:
        subject = u'ML BBS 你有新的评论'
        body = u'%s 评论了你的回复：%s' % (comment.user.name, comment.content)
        to_list = [recipient.email]
        send_text_email(subject, body, to_list)


@receiver(post_save, sender=Reply, dispatch_uid="reply_post_save")
def send_reply_message(sender, **kwargs):
    reply = kwargs['instance']

    recipient = reply.post.author
    verb = f'you get a reply from {reply.user.name}'
    message = {}
    message['recipient'] = recipient            # 消息接收人
    message['verb'] = verb                      # 消息标题
    message['description'] = reply.content_html # 评论详细内容
    message['target'] = reply.post              # 目标对象
    message['action_object'] = reply            # 评论记录
    notify.send(reply.user, **message)
    if recipient.mailnotify:
        subject = u'ML BBS 你有新的回复'
        body = u'%s 回复了你的帖子：%s' % (reply.user.name, reply.content_html)
        to_list = [recipient.email]
        send_text_email(subject, body, to_list)
