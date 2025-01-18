import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import axios from "axios";

export function makeGET<T>(url: string) {
    const token = localStorage.getItem("auth_token");
    return axios.get<T>(url, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

export function makePOST<T>(url: string, data: unknown) {
    const token = localStorage.getItem("auth_token");
    return axios.post<T>(url, data, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

export function makePUT<T>(url: string, data: unknown) {
    const token = localStorage.getItem("auth_token");
    return axios.put<T>(url, data, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

export function makeDELETE<T>(url: string) {
    const token = localStorage.getItem("auth_token");
    return axios.delete<T>(url, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

export function makePATCH<T>(url: string, data: unknown) {
    const token = localStorage.getItem("auth_token");
    return axios.patch<T>(url, data, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}


export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}
