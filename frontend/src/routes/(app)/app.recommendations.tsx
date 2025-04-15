import {createFileRoute} from '@tanstack/react-router'
import TinderCards from "@/widgets/tinder_cards/tinder_cards.tsx";

export const Route = createFileRoute('/(app)/app/recommendations')({
  component: RouteComponent,
})

function RouteComponent() {
  return <TinderCards/>
}
