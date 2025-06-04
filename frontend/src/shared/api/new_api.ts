import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";
import {paths} from "./generated/schema";

const fetchClient = createFetchClient<paths>({
	baseUrl: "http://127.0.0.1:8000",
});

export const $api = createClient(fetchClient);