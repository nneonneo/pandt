//  OpenEars version 0.913
//  http://www.politepix.com/openears
//
//  OpenEarsErrorDictionary.h
// 
//  OpenEarsErrorDictionary is a class which defines OpenEars-specific NSErrors
//
//  Copyright Halle Winkler 2010, 2011. All rights reserved.
//  http://www.politepix.com
//  Contact at http://www.politepix.com/contact
//
//  This file is licensed under the Common Development and Distribution License (CDDL) Version 1.0
//  http://www.opensource.org/licenses/cddl1.txt or see included file license.txt
//  with the single exception to the license that you may distribute executable-only versions
//  of software using OpenEars files without making source code available under the terms of CDDL Version 1.0 
//  paragraph 3.1 if source code to your software isn't otherwise available, and without including a notice in 
//  that case that that source code is available. Exception applies exclusively to compiled binary apps such as can be
//  downloaded from the App Store, and not to frameworks or systems, to which the un-altered CDDL applies
//  unless other terms are agreed to by the copyright holder.

#define kOpenEarsErrorDomain @"OpenEarsErrorDomain"

#define kOpenEarsErrorLanguageModelHasNoContentCode 100
#define kOpenEarsErrorLanguageModelHasNoContentMessage @"Requested language model has no content"
#define kOpenEarsErrorLanguageModelHasNoContent [NSError errorWithDomain:kOpenEarsErrorDomain code:kOpenEarsErrorLanguageModelHasNoContentCode userInfo:[NSDictionary dictionaryWithObject:kOpenEarsErrorLanguageModelHasNoContentMessage forKey:NSLocalizedDescriptionKey]];
