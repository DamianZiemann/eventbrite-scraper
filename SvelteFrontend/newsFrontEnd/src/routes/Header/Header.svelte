<script>
    export let menuOpen = false;
    function toggleMenu() {
        menuOpen = !menuOpen;
    }
  </script>
  
  <header class="header">
    <button class="menu-icon" aria-label="Menü öffnen" on:click={toggleMenu}>
        ☰
    </button>
    <div class="logo">Pitchload</div>
    <nav class:open={menuOpen}>
        <ul>
            <li><a href="/">News</a></li>
            <li><a href="/map">Map</a></li>
            <li><a href="/Liste">Liste</a></li>
        </ul>
    </nav>
  </header>
  
  <style>
    .header {
        font-family: 'Arial', sans-serif;
        font-style: italic;
        background-color: #fff;
        padding: 20px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        position: relative;
        z-index: 10;
    }
    .menu-icon {
        font-family: 'Arial', sans-serif;
        font-size: 1.8em;
        cursor: pointer;
        margin-right: 20px;
        padding: 10px;
        user-select: none;
        background: none;
        border: none;
        color: #333;
    }
    .logo {
        font-family: 'Arial', sans-serif;
        font-size: 1.5em;
        font-weight: bold;
    }
    nav {
        font-family: 'Arial', sans-serif;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        display: none;
    }
    nav.open {
        display: block;
    }
    nav ul {
        font-family: 'Arial', sans-serif;
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    nav ul li {
        margin: 10px 0;
    }
    nav ul li a {
        font-family: 'Arial', sans-serif;
        text-decoration: none;
        color: #333;
    }
  </style>
  