import {useGetAccessTokenFromCookieTokenGet, useLoginLoginPost} from "@/shared/api/generated/auth/auth.ts";

export const $user_api = {
	getAccessTokenFromCookieToken: useGetAccessTokenFromCookieTokenGet,
	login: useLoginLoginPost
}