from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from .models import vote
from posts.models import post


class VoteModelTest(TestCase):
    """
    Test - Vote info is saved and retrievable, users and posts have votes
    """
    def test_save_and_retrieve_votes(self):
        user1 = get_user_model().objects.create_user(
            'Jim', 'chipperdrew@gmail.com', 'pass'
        )
        user2 = get_user_model().objects.create_user(
            'Jack', 'j@gmail.com', 'pass'
        )
        post1 = post.objects.create(
            title = 'Post numero uno!', user_id=user1, text='Post 1 text'
        )

        vote1 = vote.objects.create(
            user_id=user1, post_id=post1, vote_choice=vote.VOTE_CHOICES.upvote
        )
        vote2 = vote.objects.create(
            user_id=user2, post_id=post1, vote_choice=vote.VOTE_CHOICES.downvote
        )
        saved_votes = vote.objects.all()
        self.assertEqual(saved_votes.count(), 2)

        saved_vote1 = saved_votes[0]
        saved_vote2 = saved_votes[1]
        self.assertEqual(saved_vote1.user_id, user1)
        self.assertEqual(saved_vote1.post_id, post1)
        self.assertEqual(saved_vote1.vote_choice, vote.VOTE_CHOICES.upvote)
        self.assertEqual(saved_vote2.user_id, user2)
        self.assertEqual(saved_vote2.post_id, post1)
        self.assertEqual(saved_vote2.vote_choice, vote.VOTE_CHOICES.downvote)

    def test_users_and_posts_have_votes(self):
        user1 = get_user_model().objects.create_user(
            'Jim', 'chipperdrew@gmail.com', 'pass'
        )
        user2 = get_user_model().objects.create_user(
            'Jack', 'j@gmail.com', 'pass'
        )
        post1 = post.objects.create(
            title = 'Post numero uno!', user_id=user1, text='Post 1 text'
        )

        vote1 = vote.objects.create(
            user_id=user1, post_id=post1, vote_choice=vote.VOTE_CHOICES.upvote
        )
        vote2 = vote.objects.create(
            user_id=user2, post_id=post1, vote_choice=vote.VOTE_CHOICES.downvote
        )

        all_users = get_user_model().objects.all()
        self.assertEqual(all_users.count(), 2)
        user1 = all_users[0]
        user2 = all_users[1]
        self.assertEqual(user1.votes.count(), 1)
        self.assertEqual(user2.votes.count(), 1)
        self.assertEqual(user1.votes.all()[0].vote_choice, vote.VOTE_CHOICES.upvote)
        self.assertEqual(user2.votes.all()[0].vote_choice, vote.VOTE_CHOICES.downvote)

        all_posts = post.objects.all()
        self.assertEqual(all_posts.count(), 1)
        self.assertEqual(all_posts[0].votes.count(), 2)
