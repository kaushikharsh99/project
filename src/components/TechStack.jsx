import React from 'react';
import { motion } from 'framer-motion';
import { FaReact, FaNodeJs, FaPython, FaDocker, FaAws, FaGitAlt, FaFigma, FaLinux, FaRust, FaVuejs } from 'react-icons/fa';
import { SiTypescript, SiTailwindcss, SiNextdotjs, SiMongodb, SiPostgresql, SiGo } from 'react-icons/si';

const techs = [
  { icon: FaReact, color: "#61DAFB" },
  { icon: SiNextdotjs, color: "#ffffff" },
  { icon: SiTypescript, color: "#3178C6" },
  { icon: SiTailwindcss, color: "#06B6D4" },
  { icon: FaNodeJs, color: "#339933" },
  { icon: SiMongodb, color: "#47A248" },
  { icon: SiPostgresql, color: "#4169E1" },
  { icon: FaPython, color: "#3776AB" },
  { icon: SiGo, color: "#00ADD8" },
  { icon: FaRust, color: "#DEA584" },
  { icon: FaDocker, color: "#2496ED" },
  { icon: FaAws, color: "#FF9900" },
  { icon: FaGitAlt, color: "#F05032" },
  { icon: FaFigma, color: "#F24E1E" },
  { icon: FaLinux, color: "#FCC624" },
  { icon: FaVuejs, color: "#4FC08D" },
];

const TechStack = () => {
  return (
    <div className="py-10 bg-gray-950 border-y border-gray-800 overflow-hidden relative">
      {/* Fade Gradients */}
      <div className="absolute top-0 left-0 w-32 h-full bg-gradient-to-r from-gray-950 to-transparent z-10"></div>
      <div className="absolute top-0 right-0 w-32 h-full bg-gradient-to-l from-gray-950 to-transparent z-10"></div>

      <motion.div 
        className="flex space-x-16 w-max"
        animate={{ x: [0, -1035] }} // Approximate width of half the icons
        transition={{ 
          repeat: Infinity, 
          duration: 25, 
          ease: "linear" 
        }}
      >
        {/* Duplicate list to create seamless loop */}
        {[...techs, ...techs, ...techs].map((Tech, index) => (
          <div key={index} className="flex items-center justify-center group">
            <Tech.icon 
              className="text-5xl transition-colors duration-300 group-hover:grayscale-0 filter grayscale opacity-50 group-hover:opacity-100" 
              style={{ color: Tech.color }}
            />
          </div>
        ))}
      </motion.div>
    </div>
  );
};

export default TechStack;
