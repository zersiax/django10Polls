from django.core.urlresolvers import reverse
from django.test import TestCase
import datetime
from django.utils import timezone

from .models import Question
class QuestionMethodTests(TestCase):
  def test_was_published_recently_with_future_question(self):
    # tests shouldn't return true for published_recently when the pub_date is in the future
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)
    self.assertEqual(future_question.was_published_recently(), False)
def test_was_published_recently_with_old_question(self):
    # false if test is indeed recent
  time = timezone.now() - datetime.timedelta(days=30)
  old_question = Question(pub_date=time)
  self.assertEqual(old_question.was_published_recently(), False)

def test_was_published_recently_with_recent_question(self):
    # true if indeed recent
	
  time = timezone.now() - datetime.timedelta(hours=1)
  recent_question = Question(pub_date=time)
  self.assertEqual(recent_question.was_published_recently(), True)

def create_question(question_text, days):
  # creates a question with the offset in days as the second parameter
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text,
  pub_date=time)
  
class QuestionViewTests():


  def test_index_view_with_no_questions(self):
    # a message should be displayed if there is no questions at all to displayed
	
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
	
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'], [])
  
  def test_index_view_with_a_past_question(self):
# dates in the past should be displayed on the index page
    create_question(question_text="Past question.", days=-30)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      ['<Question: Past question.>']
    )

  def test_index_view_with_a_future_question(self):
# If a publish date is in the future, obviously it should not be displayed in the present. That will create a temporal paradox
    create_question(question_text="Future question.", days=30)
    response = self.client.get(reverse('polls:index'))
    self.assertContains(response, "No polls are available.",
    status_code=200)
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_index_view_with_future_question_and_past_question(self):
# Adding questions in the past will not magically solve the above-mentioned temporal paradox ;)
    create_question(question_text="Past question.", days=-30)
    create_question(question_text="Future question.", days=30)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      ['<Question: Past question.>']
    )

  def test_index_view_with_two_past_questions(self):

# Where there is one ...there may be more. Kill it with fire! ...er...that is ...test it with diligence

    create_question(question_text="Past question 1.", days=-30)
    create_question(question_text="Past question 2.", days=-5)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      ['<Question: Past question 2.>', '<Question: Past question 1.>']
    )

class QuestionIndexDetailTests(TestCase):
  def test_detail_view_with_a_future_question(self):
# Only questions in the past may be accessed directly. No time machines allowed.
    future_question = create_question(question_text='Future question.',
    days=5)
    response = self.client.get(reverse('polls:detail',
    args=(future_question.id,)))
    self.assertEqual(response.status_code, 404)

  def test_detail_view_with_a_past_question(self):
# the detail page for a question that has been stated in the past should be neatly accessible
    past_question = create_question(question_text='Past Question.',
    days=-5)
    response = self.client.get(reverse('polls:detail',
    args=(past_question.id,)))
    self.assertContains(response, past_question.question_text,
    status_code=200)