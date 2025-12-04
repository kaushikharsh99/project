import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { posts } from '../data/posts';
import { motion } from 'framer-motion';
import { FaCalendar, FaClock, FaArrowLeft, FaTag } from 'react-icons/fa';

const BlogPost = () => {
  const { id } = useParams();
  const post = posts.find((p) => p.id === id);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [id]);

  if (!post) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
        <h2 className="text-3xl font-bold mb-4">Post Not Found</h2>
        <Link to="/blog" className="text-blue-500 hover:underline">
          Back to Blog
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-3xl mx-auto"
      >
        <Link 
          to="/blog" 
          className="inline-flex items-center text-gray-400 hover:text-white mb-8 transition-colors"
        >
          <FaArrowLeft className="mr-2" /> Back to Blog
        </Link>

        <header className="mb-10 text-center">
          <div className="flex items-center justify-center gap-2 mb-6">
            <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-sm font-medium flex items-center gap-2">
              <FaTag size={12} /> {post.category}
            </span>
          </div>
          
          <h1 className="text-3xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          
          <div className="flex items-center justify-center gap-6 text-gray-400 text-sm">
            <span className="flex items-center gap-2"><FaCalendar /> {post.date}</span>
            <span className="flex items-center gap-2"><FaClock /> {post.readTime}</span>
          </div>
        </header>

        <div className="relative h-64 md:h-96 rounded-xl overflow-hidden mb-10 shadow-2xl">
          <img 
            src={post.image} 
            alt={post.title} 
            className="w-full h-full object-cover"
          />
        </div>

        <article className="prose prose-invert prose-lg max-w-none">
          {/* Ideally, use a Markdown parser here like react-markdown. For now, rendering HTML carefully. */}
          <div dangerouslySetInnerHTML={{ __html: post.content }} />
        </article>

      </motion.div>
    </div>
  );
};

export default BlogPost;
