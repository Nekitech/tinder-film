"use client";
import {useEffect, useState} from "react";
import {easeOutExpo} from "@/shared/lib/easings.data.ts";
import {CardSwipeDirection, IsDragOffBoundary} from "@/shared/types/cards.type.ts";
import GameActionBtn from "@/features/card_custom/card_actions_btn.tsx";
import {AnimatePresence, motion} from "framer-motion";
import {$api} from "@/shared/api/new_api.ts";
import {useAuth} from "@/shared/providers/auth.provider.tsx";
import CardCustom from "@/features/card_custom/card_custom.tsx";
import {components} from "@/shared/api/generated/schema";
import {Slider} from "@/shared/components/ui/slider.tsx";
import {Checkbox} from "@/shared/components/ui/checkbox.tsx";
import {Spinner} from "@/shared/components/ui/spinner.tsx";
// import { BgPattern } from "@/components/ui";


const initialDrivenProps = {
	cardWrapperX: 0,
	buttonScaleBadAnswer: 1,
	buttonScaleGoodAnswer: 1,
	mainBgColor: "var(--color-bg-primary)",
};

const TinderCards = () => {
	const [chooseRating, setChooseRating] = useState<number>(1);
	const [isRating, setIsRating] = useState<boolean>(true);

	const [films, setFilms] = useState<components["schemas"]["RecommendationResponse"]["recommendations"]>([]);

	const {user} = useAuth()

	const {mutate: mutateLikeOrDislike} = $api.useMutation(
		"post",
		"/interactions/like_or_dislike",
		{
			onSuccess: () => {
				console.log("success like or dislike")
			},
			onError: () => {
				console.log("error like or dislike")
			}
		}
	)

	const {mutate: mutateRating} = $api.useMutation(
		"post",
		"/recommender/ratings",
		{
			onSuccess: () => {
				console.log("success rating")
			},
			onError: () => {
				console.log("error rating")
			}
		}
	)

	const {data, isPending} = $api.useQuery(
		"get",
		"/recommender/recommendations/{user_id}",
		{
			params: {
				path: {
					"user_id": String(user?.sub)
				},
				query: {
					n: 10,
					limit: 1000
				}
			}
		}
	)
	useEffect(() => {
		if (data) {
			setFilms(data.recommendations)
		}
	}, [data])
	const [direction, setDirection] = useState<CardSwipeDirection | "">("");
	const [isDragOffBoundary, setIsDragOffBoundary] =
        useState<IsDragOffBoundary>(null);
	const [cardDrivenProps, setCardDrivenProps] = useState(initialDrivenProps);
	const [isDragging, setIsDragging] = useState(false);


	const handleLikeOrDislike = (direction: CardSwipeDirection) => {
		const data = {
			user_id: Number(user?.sub) as number,
			movie_id: Number(films[films.length - 1]?.movie_id) as number,
			liked: true
		}
		switch (direction) {
		case "left":
			data["liked"] = false
			return data
		case "right":
			data["liked"] = true
			return data
		default:
			throw new Error("Unknown direction")

		}
	}

	const handleActionBtnOnClick = (direction: CardSwipeDirection) => {
		mutateLikeOrDislike({
			params: {
				query: handleLikeOrDislike(direction)
			}
		})
		if (!isRating) {
			mutateRating({
				body: {
					user_id: Number(user?.sub) as number,
					movie_id: Number(films[films.length - 1]?.movie_id) as number,
					rating: chooseRating
				}
			})
		}
		setDirection(direction);
		setIsRating(true)
	};

	useEffect(() => {
		if (["left", "right"].includes(direction)) {
			setFilms(prevState => prevState.slice(0, -1));
		}
		setDirection("");
	}, [direction]);

	const cardVariants = {
		current: {
			opacity: 1,
			y: 0,
			scale: 1,
			transition: {duration: 0.3, ease: easeOutExpo},
		},
		upcoming: {
			opacity: 0.5,
			y: 67,
			scale: 0.9,
			transition: {duration: 0.3, ease: easeOutExpo, delay: 0},
		},
		remainings: {
			opacity: 0,
			y: 20,
			scale: 0.9,
		},
		exit: {
			opacity: 0,
			x: direction === "left" ? -300 : 300,
			y: 40,
			rotate: direction === "left" ? -20 : 20,
			transition: {duration: 0.3, ease: easeOutExpo},
		},
	};

	if (isPending) {
		return <Spinner size={"large"} />;
	}

	return (
		<motion.div
			className={`flex p-5 min-h-screen h-full flex-col justify-center items-center overflow-hidden  ${
				isDragging ? "cursor-grabbing" : ""
			}`}
			style={{backgroundColor: cardDrivenProps.mainBgColor}}
		>
			<div
				id="gameUIWrapper"
				className="flex flex-col gap-6 w-full items-center justify-center relative z-10"
			>
				<div
					id="cardsWrapper"
					className="w-full aspect-[100/150] max-w-xs mb-[20px] relative z-10"
				>
					<AnimatePresence>
						{ films.map((card, i) => {
							const isLast = i === films.length - 1;
							const isUpcoming = i === films.length - 2;
							return (
								<motion.div
									key={`card-${i}`}
									id={`card-${card.movie_id}`}
									className="relative"
									variants={cardVariants}
									initial="remainings"
									animate={isLast ? "current" : isUpcoming ? "upcoming" : "remainings"}
									exit="exit"
								>
									<CardCustom
										data={{
											id: card.movie_id,
											description: "",
											image: "",
											name: card.title,
											rating: card.predicted_rating
										}}
										id={card.movie_id}
										setCardDrivenProps={setCardDrivenProps}
										setIsDragging={setIsDragging}
										isDragging={isDragging}
										isLast={isLast}
										setIsDragOffBoundary={setIsDragOffBoundary}
										setDirection={setDirection}
										handleActionBtnOnClick={handleActionBtnOnClick}
									/>
								</motion.div>
							);
						}) }
					</AnimatePresence>

				</div>
				<div
					id="actions"
					className="flex items-center justify-center w-full  gap-4 relative z-10"
				>
					<GameActionBtn
						direction="left"
						ariaLabel="swipe left"
						scale={cardDrivenProps.buttonScaleBadAnswer}
						isDragOffBoundary={isDragOffBoundary}
						onClick={() => handleActionBtnOnClick("left")}
					/>
					<GameActionBtn
						direction="right"
						ariaLabel="swipe right"
						scale={cardDrivenProps.buttonScaleGoodAnswer}
						isDragOffBoundary={isDragOffBoundary}
						onClick={() => handleActionBtnOnClick("right")}
					/>
				</div>
				<p>{ chooseRating }</p>
				<Slider
					max={5}
					min={1}
					step={0.5}
					disabled={isRating}
					className="w-1/4 cursor-pointer"
					onValueChange={(value) => {
						if (value[0]) {
							setChooseRating(value[0])
						}

					}}
				/>
				<div className={'flex items-center justify-center w-full gap-4'}>
					<p>Включить рейтинг:</p>
					<Checkbox
						className={"cursor-pointer"}
						checked={!isRating}
						onClick={() => {
							setIsRating(!isRating);
						}}
					/>
				</div>
			</div>
		</motion.div>
	);
};

export default TinderCards;