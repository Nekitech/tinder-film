import {createFileRoute} from '@tanstack/react-router'
import SignUpForm from "@/features/auth/ui/SignUpForm.tsx";

export const Route = createFileRoute('/(auth)/sign_up')({
	component: RouteComponent,
})

function RouteComponent() {
	return (
		<div className={'absolute top-[50%] left-[50%] transform -translate-y-[50%] -translate-x-[50%]'}>
			<SignUpForm />
		</div>
	)
}
