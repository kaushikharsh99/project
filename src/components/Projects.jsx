import React from 'react';
import { motion } from 'framer-motion';
import { FaGithub, FaExternalLinkAlt } from 'react-icons/fa';

const Projects = () => {
  const projects = [
    {
      title: 'E-Commerce Platform',
      description: 'A full-featured online store built with Next.js, Stripe, and Sanity CMS. Features include user authentication, cart management, and secure checkout.',
      tags: ['Next.js', 'Stripe', 'Sanity', 'Tailwind'],
      github: '#',
      demo: '#',
      image: 'https://via.placeholder.com/500x300'
    },
    {
      title: 'Task Management App',
      description: 'A productivity application helping teams collaborate efficiently. Real-time updates, drag-and-drop interface, and detailed analytics.',
      tags: ['React', 'Firebase', 'Redux', 'Material UI'],
      github: '#',
      demo: '#',
      image: 'https://via.placeholder.com/500x300'
    },
    {
      title: 'AI Content Generator',
      description: 'SaaS platform utilizing OpenAI API to generate marketing copy. Includes template management and history tracking.',
      tags: ['TypeScript', 'OpenAI', 'Node.js', 'PostgreSQL'],
      github: '#',
      demo: '#',
      image: 'https://via.placeholder.com/500x300'
    },
    {
      title: 'Portfolio Website',
      description: 'Modern portfolio site with 3D animations and interactive elements to showcase creative work.',
      tags: ['Three.js', 'React', 'GSAP', 'WebGL'],
      github: '#',
      demo: '#',
      image: 'https://via.placeholder.com/500x300'
    }
  ];

  return (
    <section id="projects" className="py-20 bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Featured Projects</h2>
          <div className="w-20 h-1 bg-blue-500 mx-auto rounded-full"></div>
          <p className="mt-4 text-gray-400 max-w-2xl mx-auto">
            A selection of projects that showcase my passion for building scalable and user-friendly applications.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {projects.map((project, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className="bg-gray-800 rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
            >
              <div className="h-48 overflow-hidden">
                <img 
                  src={project.image} 
                  alt={project.title} 
                  className="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
                />
              </div>
              
              <div className="p-6">
                <h3 className="text-xl font-bold mb-2">{project.title}</h3>
                <p className="text-gray-400 text-sm mb-4 line-clamp-3">
                  {project.description}
                </p>
                
                <div className="flex flex-wrap gap-2 mb-6">
                  {project.tags.map((tag) => (
                    <span 
                      key={tag} 
                      className="px-2 py-1 text-xs font-medium text-blue-400 bg-blue-400/10 rounded-full"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                <div className="flex justify-between items-center">
                  <a 
                    href={project.github}
                    className="text-gray-300 hover:text-white transition-colors flex items-center gap-2 text-sm"
                  >
                    <FaGithub size={16} /> Source
                  </a>
                  <a 
                    href={project.demo}
                    className="text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-2 text-sm"
                  >
                    <FaExternalLinkAlt size={14} /> Live Demo
                  </a>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Projects;
