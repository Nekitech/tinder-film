import {useForm} from "react-hook-form";
import {z} from "zod";
import {loginFormScheme} from "@/features/auth/model/scheme_login_form.ts";
import {zodResolver} from "@hookform/resolvers/zod";
import {Form, FormControl, FormField, FormItem, FormLabel, FormMessage} from "@/shared/components/ui/form";
import {Button} from "@/shared/components/ui/button";
import {Input} from "@/shared/components/ui/input";
import {useAuth} from "@/shared/providers/auth.provider.tsx";
import {useNavigate} from "@tanstack/react-router";

const LoginForm = () => {
	const {login, isAuthenticated} = useAuth()
	const navigate = useNavigate()
	const form = useForm<z.infer<typeof loginFormScheme>>({
		resolver: zodResolver(loginFormScheme),
		defaultValues: {
			username: "",
			password: ''
		},

	})

	async function onSubmit(values: z.infer<typeof loginFormScheme>) {
		await login!(values.username, values.password)

		if (isAuthenticated?.()) {
			console.log('auth success')
			navigate({
				to: '/app'
			})
		}

	}

	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 border-2 border-grey-500 rounded-2xl p-4">
				<FormField
					control={form.control}
					name="username"
					render={({field}) => (
						<FormItem>
							<FormLabel>Username</FormLabel>
							<FormControl>
								<Input type={'text'} placeholder={'at least 2 characters'} {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name="password"
					render={({field}) => (
						<FormItem>
							<FormLabel>Password</FormLabel>
							<FormControl>
								<Input type={'password'} placeholder="************" {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<Button type="submit" className={"cursor-pointer"}>Submit</Button>
			</form>
		</Form>
	);
};

export default LoginForm;