import { Outlet } from "react-router";
import Navbar from "~/components/NavBar";
import Footer from "~/components/Footer";

const links = [
    {name:'Home', ref_link: "/" },
    {name:'Generators',ref_link:'/generator'},
    {name: 'Modules', ref_link:'/module'},
    {name: "CodeEditor",  ref_link:'/codeEditor'}
]
const app_name = "Gestalt App";
function Layout() {
    return (
      <div>
        <Navbar app_name={app_name} links={links} />
        <main>
          <Outlet />
        </main>
        <Footer />
      </div>
    );
  }
  
  export default Layout;