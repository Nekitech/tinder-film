import {createContext, FC, useContext, useEffect, useState} from "react";
import {$user_api} from "@/shared/api/user.api.ts";
import {LoginResponse} from "@/shared/api/generated/fastAPI.schemas.ts";


type AuthContextType = {
    isAuthenticated: boolean
    accessToken: string | null
    login: (username: string, password: string) => Promise<LoginResponse | undefined>
    logout: () => void
    refreshToken?: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
	const authContext = useContext(AuthContext);

	if (!authContext) {
		throw new Error('useAuth must be used within the AuthProvider');
	}

	return authContext;
}

export const AuthProvider: FC<{ children: React.ReactNode }> = ({children}) => {
	const [accessToken, setAccessToken] = useState<string | null>(null)
	const {data, error} = $user_api.getAccessTokenFromCookieToken({
		request: {
			withCredentials: true,
		},
	})
	const {data: dataLogin, error: errorLogin, mutate} = $user_api.login()

	const login = async (username: string, password: string) => {
		mutate({
			data: {
				username,
				password
			}
		}, {
			onSuccess: (data) => {
				setAccessToken(data?.access_token ?? null)
			}
		})

		return dataLogin
	}

	const logout = () => {
		setAccessToken(null)
	}

	useEffect(() => {
		console.log(data, error)
		console.log(dataLogin, errorLogin)
		console.log(accessToken)
	}, [accessToken, data, dataLogin, error, errorLogin]);


	return (
		<AuthContext.Provider
			value={{
				isAuthenticated: !!accessToken,
				accessToken,
				login,
				logout,
			}}
		>
			{ children }
		</AuthContext.Provider>
	)
}