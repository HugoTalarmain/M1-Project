import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import { Button } from './Button';
import './NavBar.css';
import '../index';

function NavBar() {
    const [click, setClick] = useState(false);
    const handleClick = () => setClick(!click);
    const closeMobileMenu = () => setClick(false);
    const [button, setButton]= useState(true);
    const showButton = () => {
        if (window.innerWidth <= 960)
        {
            setButton(false);   
        }
        else
        {
            setButton(true);
        }
    };

    useEffect(()=> {
        showButton();
    },[]);

    window.addEventListener('resize', showButton);

    return (
        <>
            <nav className='navbar'>
                <div className='navbar-container'>
                    <Link to='/' className = 'navbar-logo' onClick={closeMobileMenu}>
                        KOHLER <i className='fab fa-typo3'/>
                    </Link>
                    <div className='menu-icon' onClick={handleClick}>
                        <i className={click ? 'fa fa-times' : 'fas fa-bars'}/>
                    </div>   
                    <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                        <li className='nav-item'>
                            < Link to='/presentation' className='nav-links' onClick={closeMobileMenu}>
                                Présentation
                            </Link>
                        </li>
                        <li className='nav-item'>
                            < Link to='/calcul' className='nav-links' onClick={closeMobileMenu}>
                                Calcul du bilan
                            </Link>
                        </li>
                        <li className='nav-item'>
                            < Link to='/solutions' className='nav-links' onClick={closeMobileMenu}>
                                Solutions
                            </Link>
                        </li>
                        <li className='nav-item'>
                            < Link to='/contact' className='nav-links' onClick={closeMobileMenu}>
                                Nous contacter
                            </Link>
                        </li>
                    </ul>  
                    {button && <Button buttonStyle={'btn--outline'}>Nous contacter</Button>}
                </div>
            </nav>        
        </>

    );
}

export default NavBar
