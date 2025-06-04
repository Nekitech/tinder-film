import {
	authUserCheckSelfInfoUsersMeGet,
	getAuthUserCheckSelfInfoUsersMeGetQueryKey,
	useAuthRefreshJwtRefreshPost,
	useAuthUserCheckSelfInfoUsersMeGet,
	useLoginLoginPost
} from "@/shared/api/generated/auth/auth.ts";


export const $auth_api = {
	usersMe: {
		hook: useAuthUserCheckSelfInfoUsersMeGet,
		queryKey: getAuthUserCheckSelfInfoUsersMeGetQueryKey(),
		query: authUserCheckSelfInfoUsersMeGet
	},
	login: {
		hook: useLoginLoginPost,
	},
	refresh: {
		hook: useAuthRefreshJwtRefreshPost
	}
}