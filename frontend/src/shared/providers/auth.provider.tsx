import {createContext, FC, useContext, useEffect, useState} from "react";
import {useGetAccessTokenFromCookieTokenGet, useLoginLoginPost} from "@/shared/api/generated/auth/auth.ts";


type AuthContextType = {
    isAuthenticated: boolean
    accessToken: string | null
    login: (username: string, password: string) => Promise<void>
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
	const {data, error} = useGetAccessTokenFromCookieTokenGet({
		request: {
			withCredentials: true,
		},
	})
	const {data: dataLogin, error: errorLogin, mutate} = useLoginLoginPost()

	const login = async (username: string, password: string) => {
		mutate({
			params: {
				username,
				password
			}
		}, {
			onSuccess: (data) => {
				console.log(data)
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