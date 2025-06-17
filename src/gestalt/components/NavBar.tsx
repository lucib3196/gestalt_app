"use client";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
} from "@headlessui/react";
import { Bars3Icon, BellIcon, XMarkIcon } from "@heroicons/react/24/outline";
import { PiStudent } from "react-icons/pi";
import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronDownIcon } from '@heroicons/react/20/solid'
type navigationType = {
  name: string;
  href: string;
  current: boolean;
  dropdown?: boolean
}
const navigation = [
  { name: "About", href: "/", current: true, },
  { name: "Explore", href: "/explore", current: false },
  { name: "Questions", href: "/packages", current: false },
  {
    name: "Generators", href: "/generators", current: false, dropdown: true, dropdownItems: [
      { name: "Text", href: "/generators/text_generator" },
      { name: "Image", href: "/generators/image_generator" },
      { name: "Lecture", href: "/generators/lecture_generator" }
    ]
  },
];

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}
export default function NavBar() {
  const pathname = usePathname()

  return (
    <Disclosure as="nav" className="bg-gray-800">
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="relative flex h-16 items-center justify-between">
          {/* Mobile Menu Button */}
          <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
            <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-white">
              <span className="sr-only">Open main menu</span>
              <Bars3Icon className="block h-6 w-6 group-data-open:hidden" aria-hidden="true" />
              <XMarkIcon className="hidden h-6 w-6 group-data-open:block" aria-hidden="true" />
            </DisclosureButton>
          </div>

          {/* Desktop Menu */}
          <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
            <div className="hidden sm:ml-6 sm:block">
              <div className="flex space-x-4 items-center">
                {navigation.map((item) =>
                  item.dropdown ? (
                    <Menu key={item.name}>
                      <MenuButton className="flex items-center text-white space-x-1">
                        <span>{item.name}</span>
                        <ChevronDownIcon className="h-4 w-4 fill-white/60" />
                      </MenuButton>
                      <MenuItems transition
                        anchor="bottom" className=" flex flex-col justify-center items-center mt-2 w-40 rounded-xl border border-white/20 bg-gray-800 p-1 text-white text-sm shadow-lg ring-1 ring-black/5 focus:outline-none">
                        {item.dropdownItems.map((ditem) => (
                          <MenuItem key={ditem.name}>
                            <Link
                              href={ditem.href}
                              className="block px-3 py-2 rounded-md hover:bg-white/10"
                            >
                              {ditem.name}
                            </Link>
                          </MenuItem>
                        ))}
                      </MenuItems>
                    </Menu>
                  ) : (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={`px-3 py-2 rounded-md text-base font-medium ${pathname === item.href
                        ? 'bg-gray-900 text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                        }`}
                      aria-current={pathname === item.href ? 'page' : undefined}
                    >
                      {item.name}
                    </Link>
                  )
                )}
              </div>
            </div>
          </div>

          {/* Right-side controls */}
          <div className="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
            <button
              type="button"
              className="rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
            >
              <span className="sr-only">View notifications</span>
              <BellIcon className="h-6 w-6" aria-hidden="true" />
            </button>

            {/* Profile Menu */}
            <Menu as="div" className="relative ml-3">
              <MenuButton className="flex items-center justify-center w-12 h-12 rounded-full border-4 border-white bg-gray-800 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                <span className="sr-only">Open user menu</span>
                <PiStudent size={40} color="white" />
              </MenuButton>
              <MenuItems className="absolute right-0 mt-2 w-48 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none">
                {['Your Profile', 'Settings', 'Sign out'].map((label) => (
                  <MenuItem key={label}>
                    <a
                      href="#"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      {label}
                    </a>
                  </MenuItem>
                ))}
              </MenuItems>
            </Menu>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <DisclosurePanel className="sm:hidden">
        <div className="space-y-1 px-2 pt-2 pb-3">
          {navigation.map((item) => (
            <DisclosureButton key={item.name} as={Link} href={item.href}>
              <span
                className={`block rounded-md px-3 py-2 text-base font-medium ${pathname === item.href
                  ? 'bg-gray-900 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`}
              >
                {item.name}
              </span>
            </DisclosureButton>
          ))}
        </div>
      </DisclosurePanel>
    </Disclosure>
  )
}

