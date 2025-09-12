import { AuthContext } from '../context/auth-context';
import { Navigate } from "react-router-dom";
import { useContext } from "react";
import type { JSX } from "react";

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
    const auth = useContext(AuthContext);
    if (!auth) { return <Navigate to={'/login'}/>; }

    const { isAuthenticated } = auth;
    return isAuthenticated ? children : <Navigate to='/login'/>;
};

export default ProtectedRoute;
