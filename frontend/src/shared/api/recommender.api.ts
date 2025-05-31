import {
	useRecommendRecommenderRecommendationsUserIdGet
} from "@/shared/api/generated/recommender-system/recommender-system.ts";

export const films = [
	{
		id: 1,
		name: 'Fight Club',
		description: 'The Fight Club',
		rating: 4.8
	},
	{
		id: 2,
		name: 'Fight Club 2',
		description: 'The Fight Club 2',
		rating: 4.2
	},
	{
		id: 3,
		name: 'Fight Club 3',
		description: 'The Fight Club 3',
		rating: 4.2
	}
]

export const $recommender_api = {
	getRecommendationsByUserId: () => useRecommendRecommenderRecommendationsUserIdGet
}