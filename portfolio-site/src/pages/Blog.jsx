import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { posts } from '../data/posts';
import { FaCalendar, FaClock, FaArrowRight } from 'react-icons/fa';

const Blog = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="pt-24 pb-20 bg-gray-900 min-h-screen text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Blog & Thoughts</h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Sharing my journey, tutorials, and thoughts on the latest in tech.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {posts.map((post, index) => (
            <motion.article
              key={post.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className="bg-gray-800 rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 flex flex-col"
            >
              <div className="h-48 overflow-hidden">
                <img 
                  src={post.image} 
                  alt={post.title} 
                  className="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
                />
              </div>
              
              <div className="p-6 flex-grow flex flex-col">
                <div className="flex items-center gap-4 text-sm text-blue-400 mb-3">
                  <span className="bg-blue-400/10 px-2 py-1 rounded-full">{post.category}</span>
                </div>

                <h2 className="text-xl font-bold mb-3 hover:text-blue-400 transition-colors">
                  <Link to={`/blog/${post.id}`}>{post.title}</Link>
                </h2>
                
                <p className="text-gray-400 text-sm mb-4 line-clamp-3 flex-grow">
                  {post.excerpt}
                </p>

                <div className="flex items-center justify-between text-xs text-gray-500 mt-auto pt-4 border-t border-gray-700">
                  <div className="flex items-center gap-4">
                    <span className="flex items-center gap-1"><FaCalendar /> {post.date}</span>
                    <span className="flex items-center gap-1"><FaClock /> {post.readTime}</span>
                  </div>
                </div>
                
                <Link 
                  to={`/blog/${post.id}`}
                  className="mt-4 inline-flex items-center text-blue-400 hover:text-blue-300 font-medium text-sm"
                >
                  Read More <FaArrowRight className="ml-2 text-xs" />
                </Link>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Blog;
