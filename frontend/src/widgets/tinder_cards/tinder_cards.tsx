"use client";
import {useEffect, useState} from "react";
import CardCustom from "@/features/card_custom/card_custom.tsx";
import {easeOutExpo} from "@/shared/lib/easings.data.ts";
import {CardSwipeDirection, IsDragOffBoundary} from "@/shared/types/cards.type.ts";
import GameActionBtn from "@/features/card_custom/card_actions_btn.tsx";
import {useFilmsContext} from "@/shared/store/films.store.tsx";
import {AnimatePresence, motion} from "framer-motion";
// import { BgPattern } from "@/components/ui";


const initialDrivenProps = {
    cardWrapperX: 0,
    buttonScaleBadAnswer: 1,
    buttonScaleGoodAnswer: 1,
    mainBgColor: "var(--color-grey-500)",
};

const TinderCards = () => {

    const [films, setFilms] = useFilmsContext()

    const [direction, setDirection] = useState<CardSwipeDirection | "">("");
    const [isDragOffBoundary, setIsDragOffBoundary] =
        useState<IsDragOffBoundary>(null);
    const [cardDrivenProps, setCardDrivenProps] = useState(initialDrivenProps);
    const [isDragging, setIsDragging] = useState(false);

    const handleActionBtnOnClick = (btn: CardSwipeDirection) => {
        setDirection(btn);
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
            transition: { duration: 0.3, ease: easeOutExpo },
        },
        upcoming: {
            opacity: 0.5,
            y: 67,
            scale: 0.9,
            transition: { duration: 0.3, ease: easeOutExpo, delay: 0 },
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
            transition: { duration: 0.3, ease: easeOutExpo },
        },
    };

    return (
        <motion.div
            className={`flex p-5 min-h-screen h-full flex-col justify-center items-center overflow-hidden  ${
                isDragging ? "cursor-grabbing" : ""
            }`}
            style={{ backgroundColor: cardDrivenProps.mainBgColor }}
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
                        {films.map((card, i) => {
                            const isLast = i === films.length - 1;
                            const isUpcoming = i === films.length - 2;
                            return (
                                <motion.div
                                    key={`card-${i}`}
                                    id={`card-${card.id}`}
                                    className={`relative `}
                                    variants={cardVariants}
                                    initial="remainings"
                                    animate={
                                        isLast ? "current" : isUpcoming ? "upcoming" : "remainings"
                                    }
                                    exit="exit"
                                >
                                    <CardCustom
                                        data={card}
                                        id={card.id}
                                        setCardDrivenProps={setCardDrivenProps}
                                        setIsDragging={setIsDragging}
                                        isDragging={isDragging}
                                        isLast={isLast}
                                        setIsDragOffBoundary={setIsDragOffBoundary}
                                        setDirection={setDirection}
                                    />
                                </motion.div>
                            );
                        })}
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
            </div>
        </motion.div>
    );
};

export default TinderCards;