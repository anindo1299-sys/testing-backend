import React from 'react';
import { NavLink } from 'react-router-dom';

export default function Navbar(){
    return(
        <nav className='navbar'>
            <div className='nav-brand'>
                <span>E-Com-react</span>
            </div>
            <div className='nav-links'>
                <NavLink to="/">Customer View</NavLink>
                <NavLink to="/admin">Admin</NavLink>
            </div>
        </nav>
    );    
}