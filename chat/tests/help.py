# def setUp(self):
#         self.user = models.User.objects.create_user(
#             username = 'test',
#             email = 'test@gmail.com',
#             password = 'Test1234'
#         )
#         self.redirect_to_home_url = reverse('chat:redirect-to-home')
#         self.home_url = reverse('chat:home')
#         self.login_url = reverse('chat:login')
#         self.logout_url = reverse('chat:logout')
#         self.signup_url = reverse('chat:signup')
#         self.user_home_url = reverse('chat:user-home', kwargs={"user_id":self.user.id})
#         self.user_public_chats_url = reverse('chat:user-public-chats', kwargs={"user_id":self.user.id})
#         self.user_public_chat_room_url = reverse('chat:user-public-chat-room', kwargs={"user_id":self.user.id, "url_id": self.url_id})
#         self.user_private_chats_url = reverse('chat:user-private-chats', kwargs={"user_id":self.user.id})
#         self.user_private_chat_room_url = reverse('chat:user-private-chat-room', kwargs={"user_id":self.user.id, "url_id": self.url_id})
#         self.user_private_chat_room_join_url = reverse('chat:user-private-chat-room-join', kwargs={"user_id":self.user.id, "url_id": self.url_id})
#         self.user_public_chat_room_join_url = reverse('chat:user-public-chat-room-join', kwargs={"user_id":self.user.id, "url_id": self.url_id})
#         self.user_public_chat_room_close_url = reverse('chat:user-public-chat-room-close', kwargs={"user_id":self.user.id, "url_id": self.url_id})

