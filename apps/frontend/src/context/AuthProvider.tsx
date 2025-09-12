import type { AuthProviderProps } from "../types";
import { AuthContext } from "./auth-context";
import { useState, useEffect } from "react";
import { jwtDecode } from 'jwt-decode';

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const [token, setToken] = useState<string | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const storedToken = localStorage.getItem('token');

        if (storedToken) {
            try {
                interface JWTPayload {
                    exp: number;
                }
                const decoded = jwtDecode<JWTPayload>(storedToken);

                if (decoded.exp * 1000 > Date.now()) {
                    setToken(storedToken);
                    setIsAuthenticated(true);
                } else {
                    localStorage.removeItem('token');
                }
            } catch {
                localStorage.removeItem('token');
            }
        }
    }, []);

    const login = (newToken: string) => {
        localStorage.setItem('token', newToken);
        setToken(newToken);
        setIsAuthenticated(true);
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ 
            token,
            isAuthenticated,
            login,
            logout
        }}>
            {children}
        </AuthContext.Provider>
    );
};
