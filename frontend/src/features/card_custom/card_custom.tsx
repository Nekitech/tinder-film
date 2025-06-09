"use client";

import {Dispatch, SetStateAction} from "react";

import {motion, useMotionValue, useMotionValueEvent, useTransform,} from "framer-motion";
import {Film} from "@/shared/types/films.type.ts";
import {CardSwipeDirection} from "@/shared/types/cards.type.ts";


type Props = {
    id?: number;
    data: Film;
    setCardDrivenProps: Dispatch<SetStateAction<any>>;
    setIsDragging: Dispatch<SetStateAction<any>>;
    isDragging: boolean;
    isLast: boolean;
    setIsDragOffBoundary: Dispatch<SetStateAction<any>>;
    setDirection: Dispatch<SetStateAction<any>>;
    handleActionBtnOnClick: (
        direction: CardSwipeDirection,
    ) => void
};


const CardCustom = ({
	id,
	data,
	setCardDrivenProps,
	setIsDragging,
	isDragging,
	setIsDragOffBoundary,
	setDirection,
	handleActionBtnOnClick
}: Props) => {

	const x = useMotionValue(0);

	const offsetBoundary = 150;

	const inputX = [offsetBoundary * -1, 0, offsetBoundary];
	const outputX = [-200, 0, 200];
	const outputY = [50, 0, 50];
	const outputRotate = [-40, 0, 40];
	const outputActionScaleBadAnswer = [3, 1, 0.3];
	const outputActionScaleRightAnswer = [0.3, 1, 3];


	const drivenX = useTransform(x, inputX, outputX);
	const drivenY = useTransform(x, inputX, outputY);
	const drivenRotation = useTransform(x, inputX, outputRotate);
	const drivenActionLeftScale = useTransform(
		x,
		inputX,
		outputActionScaleBadAnswer
	);
	const drivenActionRightScale = useTransform(
		x,
		inputX,
		outputActionScaleRightAnswer
	);

	useMotionValueEvent(x, "change", (latest) => {
		setCardDrivenProps((state: any) => ({
			...state,
			cardWrapperX: latest,
			buttonScaleBadAnswer: drivenActionLeftScale,
			buttonScaleGoodAnswer: drivenActionRightScale,
		}));
	});

	return (
		<>
			<motion.div
				id={`cardDrivenWrapper-${id}`}
				className="absolute bg-white border-4 border-secondary-green  p-8 rounded-lg text-center w-full aspect-[100/150] pointer-events-none text-black origin-bottom shadow-card select-none"
				style={{
					y: drivenY,
					rotate: drivenRotation,
					x: drivenX,
				}}
			>
				<p className={'text-green-900'}>{ data.name }</p>

				<div
					id="illustration"
					className="w-full mx-auto max-w-[250px] aspect-square rounded-full relative"
				>
					{ /*<div*/ }
					{ /*    id="imgPlaceholder"*/ }
					{ /*    className="bg-gameSwipe-neutral absolute object-cover w-full h-full"*/ }
					{ /*    style={{*/ }
					{ /*        maskImage: `url('/images/gamecard-image-mask.png')`,*/ }
					{ /*        WebkitMaskImage: `url(/images/gamecard-image-mask.png)`,*/ }
					{ /*        maskSize: "contain",*/ }
					{ /*        WebkitMaskSize: "contain",*/ }
					{ /*        maskRepeat: "no-repeat",*/ }
					{ /*        WebkitMaskRepeat: "no-repeat",*/ }
					{ /*    }}*/ }
					{ /*></div>*/ }
				</div>
			</motion.div>

			<motion.div
				id={`cardDriverWrapper-${id}`}
				className={`absolute w-full aspect-[100/150] ${
					!isDragging ? "hover:cursor-grab" : ""
				}`}
				drag="x"
				dragSnapToOrigin
				dragElastic={0.06}
				dragConstraints={{left: 0, right: 0}}
				dragTransition={{bounceStiffness: 1000, bounceDamping: 50}}
				onDragStart={() => setIsDragging(true)}
				onDrag={(_, info) => {
					const offset = info.offset.x;

					if (offset < 0 && offset < offsetBoundary * -1) {
						setIsDragOffBoundary("left");
					} else if (offset > 0 && offset > offsetBoundary) {
						setIsDragOffBoundary("right");
					} else {
						setIsDragOffBoundary(null);
					}
				}}
				onDragEnd={(_, info) => {
					setIsDragging(false);
					setIsDragOffBoundary(null);
					const isOffBoundary =
                        info.offset.x > offsetBoundary || info.offset.x < -offsetBoundary;
					const direction = info.offset.x > 0 ? "right" : "left";

					if (isOffBoundary) {
						handleActionBtnOnClick(direction)
						setDirection(direction);
					}
				}}
				style={{x}}
			/>
		</>
	);
};

export default CardCustom;