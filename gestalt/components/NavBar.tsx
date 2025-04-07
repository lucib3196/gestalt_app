"use client";

import Link from "next/link";
import { Navbar as BSNavbar, Nav, Container } from "react-bootstrap";

type LinkInfo = {
  name: string;
  path: string;
};

type NavBarProps = {
  app_name: string;
  links: LinkInfo[];
};

const NavBar = ({ app_name, links }: NavBarProps) => {
  function handleLinks() {
    return links.map((link, idx) => (
      <Nav.Link as={Link} href={link.path} key={idx}>
        {link.name}
      </Nav.Link>
    ));
  }

  return (
    <BSNavbar bg="light" expand="lg">
      <Container fluid>
        <BSNavbar.Brand as={Link} href="/">
          {app_name}
        </BSNavbar.Brand>
        <BSNavbar.Toggle aria-controls="navbar-nav" />
        <BSNavbar.Collapse id="navbar-nav">
          <Nav className="me-auto">
            {handleLinks()}
            {/* Placeholder for future sections */}
          </Nav>
        </BSNavbar.Collapse>
      </Container>
    </BSNavbar>
  );
};

export default NavBar;
