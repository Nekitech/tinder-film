import {useForm} from "react-hook-form";
import {z} from "zod";
import {loginFormScheme} from "@/features/auth/model/scheme_login_form.ts";
import {zodResolver} from "@hookform/resolvers/zod";
import {Form, FormControl, FormField, FormItem, FormLabel, FormMessage} from "@/shared/components/ui/form";
import {Button} from "@/shared/components/ui/button";
import {Input} from "@/shared/components/ui/input";
import {useAuth} from "@/shared/providers/auth.provider.tsx";
import {useEffect} from "react";

const LoginForm = () => {
	const {login, accessToken} = useAuth()
	const form = useForm<z.infer<typeof loginFormScheme>>({
		resolver: zodResolver(loginFormScheme),
		defaultValues: {
			username: "",
			password: ''
		},

	})

	function onSubmit(values: z.infer<typeof loginFormScheme>) {

		login(values.username, values.password)
	}

	useEffect(() => {
		console.log(accessToken)
	}, []);
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
				<Button type="submit">Submit</Button>
			</form>
		</Form>
	);
};

export default LoginForm;