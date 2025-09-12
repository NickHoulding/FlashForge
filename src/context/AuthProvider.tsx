import type { AuthProviderProps } from "../types";
import { AuthContext } from "./auth-context";
import { useState, useEffect } from "react";
import { jwtDecode } from 'jwt-decode';

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('token');

        if (token) {
            try {
                interface JWTPayload {
                    exp: number;
                }
                const decoded = jwtDecode<JWTPayload>(token);

                if (decoded.exp * 1000 > Date.now()) {
                    setIsAuthenticated(true);
                } else {
                    localStorage.removeItem('token');
                }
            } catch {
                localStorage.removeItem('token');
            }
        }
    }, []);

    return (
        <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated }}>
            {children}
        </AuthContext.Provider>
    );
};
