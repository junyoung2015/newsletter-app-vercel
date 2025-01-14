"use client";

import {
  Button,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  NavbarMenu,
  NavbarMenuItem,
  NavbarMenuToggle,
  Navbar as NextUINavBar,
  User,
} from "@nextui-org/react";
import { link } from "@nextui-org/theme";
import NextLink from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { FC, useEffect, useState } from "react";
import { ThemeSwitch } from "@/components/theme-switch";
import { clsx } from "@/utils/clsx";

interface MenuItems {
  label: string;
  href: string;
  disabled?: boolean;
}

const menuItems: MenuItems[] = [
  { label: "Home", href: "/" },
  { label: "About", href: "/about" },
  { label: "Create", href: "/create-newsletter" },
  // { label: "Showcase", href: "/showcase", disabled: true },
  // { label: "Pricing", href: "/pricing", disabled: true },
];

const navLinkClasses = clsx(
  link({ color: "foreground", size: "lg", underline: "hover" }),
  "data-[active=true]:text-primary",
);

export interface NavbarProps {
  email: string | null;
}

const NavBar: FC<NavbarProps> = ({ email }) => {
  const [isMenuOpen, setIsMenuOpen] = useState<boolean | undefined>(false);
  const pathname = usePathname();
  const router = useRouter();
  const username = email ? email.slice(0, email.indexOf("@")) : null;

  useEffect(() => {
    if (username === null && !["/", "/login"].includes(pathname)) {
      alert("Please login to access this page.");
      router.push("/login");
    }
  }, [username, pathname]);

  useEffect(() => {
    if (isMenuOpen) {
      setIsMenuOpen(false);
    }
  }, [pathname]);

  return (
    <NextUINavBar
      className={clsx({
        "z-[100001]": isMenuOpen,
      })}
      maxWidth="xl"
      position="sticky"
      isMenuOpen={isMenuOpen}
      onMenuOpenChange={setIsMenuOpen}
    >
      <NavbarContent className="basis-1/5 sm:basis-full" justify="start">
        <NavbarBrand>
          <NextLink
            aria-label="Home"
            className="flex items-center justify-start gap-2 transition-opacity tap-highlight-transparent active:opacity-50"
            href="/"
          >
            <p className="text-3xl font-semibold text-inherit">Easolve</p>
          </NextLink>
        </NavbarBrand>
        <ul className="hidden items-center justify-start gap-6 lg:flex">
          {menuItems.map(({ label, href, disabled }, index) => (
            <NavbarMenuItem key={`${label}-${index}`}>
              <NextLink
                className={clsx([
                  navLinkClasses,
                  disabled && "pointer-events-none no-underline",
                ])}
                color="foreground"
                data-active={pathname === href}
                href={href}
              >
                {label}
              </NextLink>
            </NavbarMenuItem>
          ))}
        </ul>
      </NavbarContent>

      <NavbarContent className="flex w-full gap-2 sm:hidden" justify="end">
        {username === null ? (
          <NavbarItem className="flex h-full items-center">
            <Button color="primary" size="sm">
              <NextLink color="foreground" href="/login">
                Login
              </NextLink>
            </Button>
          </NavbarItem>
        ) : (
          <NavbarItem className="flex h-full items-center">
            <User
              avatarProps={{
                name: username,
              }}
              name={username}
              onClick={() => router.push("/profile")}
            />
          </NavbarItem>
        )}
        <NavbarItem className="flex h-full items-center">
          <ThemeSwitch />
        </NavbarItem>
        <NavbarItem className="h-full w-10">
          <NavbarMenuToggle
            aria-label={isMenuOpen ? "Close menu" : "Open menu"}
            className="h-full w-full pt-1"
          />
        </NavbarItem>
      </NavbarContent>

      <NavbarContent
        className="hidden basis-1/5 sm:flex sm:basis-full"
        justify="end"
      >
        {username === null ? (
          <NavbarItem className="flex h-full items-center">
            <Button color="primary" size="sm">
              <NextLink color="foreground" href="/login">
                Login
              </NextLink>
            </Button>
          </NavbarItem>
        ) : (
          <NavbarItem className="flex h-full items-center">
            <User
              avatarProps={{
                name: username,
              }}
              classNames={{
                base: "cursor-pointer",
                name: "cursor-pointer",
                wrapper: "cursor-pointer",
              }}
              name={username}
              onClick={() => router.push("/profile")}
            />
          </NavbarItem>
        )}
        <NavbarItem className="hidden sm:flex">
          <ThemeSwitch />
        </NavbarItem>
        <NavbarMenuToggle
          aria-label={isMenuOpen ? "Close menu" : "Open menu"}
          className="ml-4 hidden sm:flex lg:hidden"
        />
      </NavbarContent>

      <NavbarMenu>
        {menuItems.map(({ label, href, disabled }, index) => (
          <NavbarMenuItem key={`${label}-${index}`}>
            <NextLink
              className={clsx([
                navLinkClasses,
                disabled && "pointer-events-none no-underline",
              ])}
              color="foreground"
              data-active={pathname === href}
              href={href}
            >
              {label}
            </NextLink>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </NextUINavBar>
  );
};

export default NavBar;
