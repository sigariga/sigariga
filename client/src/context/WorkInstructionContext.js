import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';

// Initial state
const initialState = {
  currentDocument: null,
  documents: [],
  templates: [],
  contentLibrary: {},
  flowcharts: [],
  activeTemplate: null,
  selectedContent: [],
  chatHistory: [],
  isLoading: false,
  error: null,
  preferences: {
    autoSave: true,
    showLineNumbers: false,
    theme: 'light',
    spellCheck: true,
  }
};

// Action types
const ACTION_TYPES = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
  
  // Document actions
  CREATE_DOCUMENT: 'CREATE_DOCUMENT',
  UPDATE_DOCUMENT: 'UPDATE_DOCUMENT',
  DELETE_DOCUMENT: 'DELETE_DOCUMENT',
  SET_CURRENT_DOCUMENT: 'SET_CURRENT_DOCUMENT',
  LOAD_DOCUMENTS: 'LOAD_DOCUMENTS',
  
  // Template actions
  LOAD_TEMPLATES: 'LOAD_TEMPLATES',
  SET_ACTIVE_TEMPLATE: 'SET_ACTIVE_TEMPLATE',
  CREATE_TEMPLATE: 'CREATE_TEMPLATE',
  UPDATE_TEMPLATE: 'UPDATE_TEMPLATE',
  DELETE_TEMPLATE: 'DELETE_TEMPLATE',
  
  // Content library actions
  LOAD_CONTENT_LIBRARY: 'LOAD_CONTENT_LIBRARY',
  ADD_CONTENT_ITEM: 'ADD_CONTENT_ITEM',
  UPDATE_CONTENT_ITEM: 'UPDATE_CONTENT_ITEM',
  DELETE_CONTENT_ITEM: 'DELETE_CONTENT_ITEM',
  SET_SELECTED_CONTENT: 'SET_SELECTED_CONTENT',
  
  // Flowchart actions
  LOAD_FLOWCHARTS: 'LOAD_FLOWCHARTS',
  CREATE_FLOWCHART: 'CREATE_FLOWCHART',
  UPDATE_FLOWCHART: 'UPDATE_FLOWCHART',
  DELETE_FLOWCHART: 'DELETE_FLOWCHART',
  
  // Chat actions
  ADD_CHAT_MESSAGE: 'ADD_CHAT_MESSAGE',
  CLEAR_CHAT_HISTORY: 'CLEAR_CHAT_HISTORY',
  
  // Preferences
  UPDATE_PREFERENCES: 'UPDATE_PREFERENCES',
};

// Reducer function
function workInstructionReducer(state, action) {
  switch (action.type) {
    case ACTION_TYPES.SET_LOADING:
      return { ...state, isLoading: action.payload };
      
    case ACTION_TYPES.SET_ERROR:
      return { ...state, error: action.payload, isLoading: false };
      
    case ACTION_TYPES.CLEAR_ERROR:
      return { ...state, error: null };
      
    // Document actions
    case ACTION_TYPES.CREATE_DOCUMENT:
      const newDocument = {
        id: uuidv4(),
        title: action.payload.title || 'New Work Instruction',
        content: action.payload.content || [],
        template: action.payload.template || null,
        metadata: {
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          author: action.payload.author || 'Unknown',
          version: '1.0',
          status: 'draft',
          ...action.payload.metadata
        }
      };
      return {
        ...state,
        documents: [...state.documents, newDocument],
        currentDocument: newDocument
      };
      
    case ACTION_TYPES.UPDATE_DOCUMENT:
      const updatedDocuments = state.documents.map(doc =>
        doc.id === action.payload.id
          ? {
              ...doc,
              ...action.payload,
              metadata: {
                ...doc.metadata,
                ...action.payload.metadata,
                updatedAt: new Date().toISOString()
              }
            }
          : doc
      );
      return {
        ...state,
        documents: updatedDocuments,
        currentDocument: state.currentDocument?.id === action.payload.id
          ? updatedDocuments.find(doc => doc.id === action.payload.id)
          : state.currentDocument
      };
      
    case ACTION_TYPES.DELETE_DOCUMENT:
      return {
        ...state,
        documents: state.documents.filter(doc => doc.id !== action.payload),
        currentDocument: state.currentDocument?.id === action.payload ? null : state.currentDocument
      };
      
    case ACTION_TYPES.SET_CURRENT_DOCUMENT:
      return { ...state, currentDocument: action.payload };
      
    case ACTION_TYPES.LOAD_DOCUMENTS:
      return { ...state, documents: action.payload };
      
    // Template actions
    case ACTION_TYPES.LOAD_TEMPLATES:
      return { ...state, templates: action.payload };
      
    case ACTION_TYPES.SET_ACTIVE_TEMPLATE:
      return { ...state, activeTemplate: action.payload };
      
    case ACTION_TYPES.CREATE_TEMPLATE:
      return { ...state, templates: [...state.templates, action.payload] };
      
    case ACTION_TYPES.UPDATE_TEMPLATE:
      return {
        ...state,
        templates: state.templates.map(template =>
          template.id === action.payload.id ? action.payload : template
        )
      };
      
    case ACTION_TYPES.DELETE_TEMPLATE:
      return {
        ...state,
        templates: state.templates.filter(template => template.id !== action.payload)
      };
      
    // Content library actions
    case ACTION_TYPES.LOAD_CONTENT_LIBRARY:
      return { ...state, contentLibrary: action.payload };
      
    case ACTION_TYPES.ADD_CONTENT_ITEM:
      const { category, item } = action.payload;
      return {
        ...state,
        contentLibrary: {
          ...state.contentLibrary,
          [category]: [...(state.contentLibrary[category] || []), item]
        }
      };
      
    case ACTION_TYPES.UPDATE_CONTENT_ITEM:
      const { category: updateCategory, item: updateItem } = action.payload;
      return {
        ...state,
        contentLibrary: {
          ...state.contentLibrary,
          [updateCategory]: state.contentLibrary[updateCategory].map(item =>
            item.id === updateItem.id ? updateItem : item
          )
        }
      };
      
    case ACTION_TYPES.DELETE_CONTENT_ITEM:
      const { category: deleteCategory, itemId } = action.payload;
      return {
        ...state,
        contentLibrary: {
          ...state.contentLibrary,
          [deleteCategory]: state.contentLibrary[deleteCategory].filter(item => item.id !== itemId)
        }
      };
      
    case ACTION_TYPES.SET_SELECTED_CONTENT:
      return { ...state, selectedContent: action.payload };
      
    // Flowchart actions
    case ACTION_TYPES.LOAD_FLOWCHARTS:
      return { ...state, flowcharts: action.payload };
      
    case ACTION_TYPES.CREATE_FLOWCHART:
      return { ...state, flowcharts: [...state.flowcharts, action.payload] };
      
    case ACTION_TYPES.UPDATE_FLOWCHART:
      return {
        ...state,
        flowcharts: state.flowcharts.map(flowchart =>
          flowchart.id === action.payload.id ? action.payload : flowchart
        )
      };
      
    case ACTION_TYPES.DELETE_FLOWCHART:
      return {
        ...state,
        flowcharts: state.flowcharts.filter(flowchart => flowchart.id !== action.payload)
      };
      
    // Chat actions
    case ACTION_TYPES.ADD_CHAT_MESSAGE:
      return {
        ...state,
        chatHistory: [...state.chatHistory, action.payload]
      };
      
    case ACTION_TYPES.CLEAR_CHAT_HISTORY:
      return { ...state, chatHistory: [] };
      
    // Preferences
    case ACTION_TYPES.UPDATE_PREFERENCES:
      return {
        ...state,
        preferences: { ...state.preferences, ...action.payload }
      };
      
    default:
      return state;
  }
}

// Create context
const WorkInstructionContext = createContext();

// Provider component
export function WorkInstructionProvider({ children }) {
  const [state, dispatch] = useReducer(workInstructionReducer, initialState);

  // Load initial data
  useEffect(() => {
    loadTemplates();
    loadContentLibrary();
    loadFlowcharts();
    loadPreferences();
  }, []);

  // Auto-save functionality
  useEffect(() => {
    if (state.preferences.autoSave && state.currentDocument) {
      const timer = setTimeout(() => {
        saveDocument(state.currentDocument);
      }, 5000); // Auto-save every 5 seconds

      return () => clearTimeout(timer);
    }
  }, [state.currentDocument, state.preferences.autoSave]);

  // API functions
  const loadTemplates = async () => {
    try {
      dispatch({ type: ACTION_TYPES.SET_LOADING, payload: true });
      const response = await fetch('/api/templates');
      const templates = await response.json();
      dispatch({ type: ACTION_TYPES.LOAD_TEMPLATES, payload: templates });
    } catch (error) {
      dispatch({ type: ACTION_TYPES.SET_ERROR, payload: error.message });
    } finally {
      dispatch({ type: ACTION_TYPES.SET_LOADING, payload: false });
    }
  };

  const loadContentLibrary = async () => {
    try {
      const response = await fetch('/api/content');
      const content = await response.json();
      dispatch({ type: ACTION_TYPES.LOAD_CONTENT_LIBRARY, payload: content });
    } catch (error) {
      dispatch({ type: ACTION_TYPES.SET_ERROR, payload: error.message });
    }
  };

  const loadFlowcharts = async () => {
    try {
      const response = await fetch('/api/flowchart');
      const flowcharts = await response.json();
      dispatch({ type: ACTION_TYPES.LOAD_FLOWCHARTS, payload: flowcharts });
    } catch (error) {
      dispatch({ type: ACTION_TYPES.SET_ERROR, payload: error.message });
    }
  };

  const loadPreferences = () => {
    try {
      const savedPreferences = localStorage.getItem('workInstructionPreferences');
      if (savedPreferences) {
        const preferences = JSON.parse(savedPreferences);
        dispatch({ type: ACTION_TYPES.UPDATE_PREFERENCES, payload: preferences });
      }
    } catch (error) {
      console.warn('Failed to load preferences:', error);
    }
  };

  const saveDocument = async (document) => {
    try {
      // Simulate API call - replace with actual API
      const savedDoc = { ...document, lastSaved: new Date().toISOString() };
      dispatch({ type: ACTION_TYPES.UPDATE_DOCUMENT, payload: savedDoc });
      return savedDoc;
    } catch (error) {
      dispatch({ type: ACTION_TYPES.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  const createDocument = (documentData) => {
    dispatch({ type: ACTION_TYPES.CREATE_DOCUMENT, payload: documentData });
  };

  const updateDocument = (documentData) => {
    dispatch({ type: ACTION_TYPES.UPDATE_DOCUMENT, payload: documentData });
  };

  const deleteDocument = (documentId) => {
    dispatch({ type: ACTION_TYPES.DELETE_DOCUMENT, payload: documentId });
  };

  const setCurrentDocument = (document) => {
    dispatch({ type: ACTION_TYPES.SET_CURRENT_DOCUMENT, payload: document });
  };

  const setActiveTemplate = (template) => {
    dispatch({ type: ACTION_TYPES.SET_ACTIVE_TEMPLATE, payload: template });
  };

  const addChatMessage = (message) => {
    const chatMessage = {
      id: uuidv4(),
      ...message,
      timestamp: new Date().toISOString()
    };
    dispatch({ type: ACTION_TYPES.ADD_CHAT_MESSAGE, payload: chatMessage });
  };

  const clearChatHistory = () => {
    dispatch({ type: ACTION_TYPES.CLEAR_CHAT_HISTORY });
  };

  const updatePreferences = (newPreferences) => {
    const updatedPreferences = { ...state.preferences, ...newPreferences };
    dispatch({ type: ACTION_TYPES.UPDATE_PREFERENCES, payload: updatedPreferences });
    
    // Save to localStorage
    try {
      localStorage.setItem('workInstructionPreferences', JSON.stringify(updatedPreferences));
    } catch (error) {
      console.warn('Failed to save preferences:', error);
    }
  };

  const clearError = () => {
    dispatch({ type: ACTION_TYPES.CLEAR_ERROR });
  };

  // Context value
  const contextValue = {
    ...state,
    actions: {
      createDocument,
      updateDocument,
      deleteDocument,
      setCurrentDocument,
      saveDocument,
      setActiveTemplate,
      loadTemplates,
      loadContentLibrary,
      loadFlowcharts,
      addChatMessage,
      clearChatHistory,
      updatePreferences,
      clearError,
    }
  };

  return (
    <WorkInstructionContext.Provider value={contextValue}>
      {children}
    </WorkInstructionContext.Provider>
  );
}

// Custom hook to use the context
export function useWorkInstruction() {
  const context = useContext(WorkInstructionContext);
  if (!context) {
    throw new Error('useWorkInstruction must be used within a WorkInstructionProvider');
  }
  return context;
}

export default WorkInstructionContext;