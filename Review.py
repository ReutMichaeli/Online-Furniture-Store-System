class Review:
    def __init__(self, customer_id, review, rating):
        '''data initialization'''
        self.customer_id = customer_id
        self.review = review
        self.rating = int(rating)