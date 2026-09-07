from django.db import models
from django.db.models import Q, Count
from apps.accounts.models import User
from apps.catalog.models import Product, ProductQuestion, ProductAnswer
from apps.orders.models import OrderItem

class ProductQuestionVote(models.Model):
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'user')


class ProductAnswerVote(models.Model):
    answer = models.ForeignKey(ProductAnswer, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_votes')
    is_helpful = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('answer', 'user')


class QAService:
    @staticmethod
    def ask_question(product, user, question_text):
        text = (question_text or '').strip()
        if len(text) < 5:
            raise ValueError("Question must be at least 5 characters long.")
        if len(text) > 1000:
            raise ValueError("Question cannot exceed 1000 characters.")

        return ProductQuestion.objects.create(
            product=product,
            user=user,
            question_text=text,
            is_approved=True
        )

    @staticmethod
    def answer_question(question, user, answer_text, is_seller=False):
        text = (answer_text or '').strip()
        if len(text) < 3:
            raise ValueError("Answer must be at least 3 characters long.")
        if len(text) > 2000:
            raise ValueError("Answer cannot exceed 2000 characters.")

        # Check if user is verified buyer
        is_buyer = OrderItem.objects.filter(
            order__user=user,
            variant__product=question.product,
            item_status__in=['DELIVERED', 'SHIPPED']
        ).exists()

        is_product_seller = (question.product.seller.user_id == user.id) or is_seller

        return ProductAnswer.objects.create(
            question=question,
            user=user,
            answer_text=text,
            is_seller_answer=is_product_seller
        )

    @staticmethod
    def vote_question(question, user):
        vote, created = ProductQuestionVote.objects.get_or_create(question=question, user=user)
        if not created:
            vote.delete()
            return False
        return True

    @staticmethod
    def vote_answer(answer, user, is_helpful=True):
        vote, created = ProductAnswerVote.objects.update_or_create(
            answer=answer,
            user=user,
            defaults={'is_helpful': is_helpful}
        )
        return vote

    @staticmethod
    def get_product_qa(product, query=None, limit=10):
        qs = ProductQuestion.objects.filter(product=product, is_approved=True).prefetch_related(
            'answers', 'answers__user', 'votes'
        ).annotate(
            vote_count=Count('votes')
        ).order_by('-vote_count', '-created_at')

        if query:
            q_clean = query.strip()
            if q_clean:
                qs = qs.filter(
                    Q(question_text__icontains=q_clean) |
                    Q(answers__answer_text__icontains=q_clean)
                ).distinct()

        return qs[:limit]
