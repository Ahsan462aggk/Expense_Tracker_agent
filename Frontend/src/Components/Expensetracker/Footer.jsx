import React from 'react';
import { Github, Linkedin, Twitter } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const socialLinks = [
    { 
      icon: Github, 
      href: "#", 
      label: "GitHub" 
    },
    { 
      icon: Linkedin, 
      href: "#", 
      label: "LinkedIn" 
    },
    { 
      icon: Twitter, 
      href: "#", 
      label: "Twitter" 
    }
  ];

  return (
    <footer className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          {/* Copyright */}
          <div className="text-sm tracking-wider opacity-90">
            &copy; {currentYear} ExpenseTracker. All Rights Reserved.
          </div>

          {/* Social Links */}
          <div className="flex space-x-4">
            {socialLinks.map((social) => (
              <a
                key={social.label}
                href={social.href}
                target="_blank"
                rel="noopener noreferrer"
                className="
                  text-white/80 hover:text-white 
                  transition-colors duration-300 
                  hover:scale-110 active:scale-95
                  flex items-center justify-center
                "
                aria-label={social.label}
              >
                <social.icon size={20} />
              </a>
            ))}
          </div>

          {/* Additional Links */}
          <div className="flex space-x-4 text-sm">
            <a 
              href="#" 
              className="
                text-white/80 hover:text-white 
                transition-colors duration-300
              "
            >
              Privacy Policy
            </a>
            <a 
              href="#" 
              className="
                text-white/80 hover:text-white 
                transition-colors duration-300
              "
            >
              Terms of Service
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;