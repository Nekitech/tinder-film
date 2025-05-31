import {motion} from "framer-motion";
import SvgIconAnswerBad from "@/assets/svg/icon-answer-bad.svg";
import SvgIconAnswerGood from "@/assets/svg/icon-answer-good.svg";
import {IsDragOffBoundary} from "@/shared/types/cards.type.ts";


const actionPropsMatrix = {
	left: {
		ariaLabel: "Swipe Left",
		bgColorClass: "bg-accent-red",
		icon: SvgIconAnswerBad,
		iconBaseColorClass: "text-[#701823]",
	},
	right: {
		ariaLabel: "Swipe Right",
		bgColorClass: "bg-accent-green",
		icon: SvgIconAnswerGood,
		iconBaseColorClass: "text-[#2C5B10]",
	},
};

const shadowStyles = {
	left: `shadow-[0_0_30px_var(--color-accent-red),0_0_60px_var(--color-accent-red)]`,
	right: `shadow-[0_0_30px_var(--color-accent-green),0_0_60px_var(--color-accent-green)]`,
};

type Props = {
    ariaLabel: string;
    scale: number;
    direction: "left" | "right";
    isDragOffBoundary: IsDragOffBoundary;
    onClick: () => void;
};

const GameActionBtn = ({
	scale,
	direction,
	isDragOffBoundary = null,
	onClick,
}: Props) => {
	const icon_element = actionPropsMatrix[direction!].icon;

	return (
		<motion.button onClick={onClick} whileTap={{scale: 0.9}}>
			<motion.div
				className={`cursor-pointer flex items-center \
				justify-center w-[60px] h-[60px] rounded-full ${actionPropsMatrix[direction].bgColorClass} 
				opacity-90
            	${shadowStyles[direction]}`}
				style={{scale: scale}}
			>
				<img
					alt={'icon'}
					src={icon_element}
					className={`w-[24px] h-[24px] duration-100 ease-out ${
						isDragOffBoundary != null && isDragOffBoundary === direction
							? "text-white"
							: actionPropsMatrix[direction!].iconBaseColorClass
					}`}
				/>
			</motion.div>
		</motion.button>
	);
};

export default GameActionBtn;
