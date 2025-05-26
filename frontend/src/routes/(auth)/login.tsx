import {createFileRoute} from '@tanstack/react-router'
import LoginForm from "@/features/auth/ui/LoginForm.tsx";

export const Route = createFileRoute('/(auth)/login')({
	component: RouteComponent,
})

function RouteComponent() {
	return (
		<div className={'absolute top-[50%] left-[50%] transform -translate-y-[50%] -translate-x-[50%]'}>
			<LoginForm />
		</div>
	)
}
