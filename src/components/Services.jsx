import React from 'react';
import { motion } from 'framer-motion';
import { FaDesktop, FaMobileAlt, FaPalette, FaRocket } from 'react-icons/fa';

const services = [
  {
    title: "Web Development",
    icon: FaDesktop,
    description: "Building fast, responsive, and scalable websites using modern frameworks like React and Next.js.",
    features: ["Custom Frontend", "API Integration", "Performance Optimization"]
  },
  {
    title: "Mobile Apps",
    icon: FaMobileAlt,
    description: "Creating native-like mobile experiences for iOS and Android using cross-platform technologies.",
    features: ["React Native", "Flutter", "PWA Development"]
  },
  {
    title: "UI/UX Design",
    icon: FaPalette,
    description: "Designing intuitive and visually appealing interfaces that prioritize user experience and accessibility.",
    features: ["Wireframing", "Prototyping", "Design Systems"]
  },
  {
    title: "SEO & Performance",
    icon: FaRocket,
    description: "Optimizing web applications for search engines and speed to ensure maximum visibility and retention.",
    features: ["Technical SEO", "Core Web Vitals", "Analytics Setup"]
  }
];

const Services = () => {
  return (
    <section id="services" className="py-24 bg-gray-950 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
         <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-4"><span className="text-blue-500">04.</span> What I Do</h2>
          <div className="h-1 w-20 bg-blue-500 mx-auto rounded-full"></div>
          <p className="mt-4 text-gray-400 max-w-2xl mx-auto">
            I help businesses and individuals bring their ideas to life with a comprehensive range of technical services.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {services.map((service, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className="bg-gray-900 p-8 rounded-xl border border-gray-800 hover:border-blue-500 transition-all duration-300 group hover:-translate-y-2"
            >
              <div className="w-14 h-14 bg-blue-500/10 rounded-lg flex items-center justify-center mb-6 group-hover:bg-blue-500 transition-colors duration-300">
                <service.icon className="text-2xl text-blue-500 group-hover:text-white transition-colors duration-300" />
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3">{service.title}</h3>
              <p className="text-gray-400 text-sm mb-6 leading-relaxed">
                {service.description}
              </p>
              
              <ul className="space-y-2">
                {service.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center text-gray-500 text-xs">
                    <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-2"></span>
                    {feature}
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;
