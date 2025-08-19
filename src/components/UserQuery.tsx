import type { UserQueryProps } from '../types';

const UserQuery = ({ content }: UserQueryProps) => {
    return <div className="user-query-root">
        <p className="user-query-text">
            {content}
        </p>
    </div>;
};

export default UserQuery;
