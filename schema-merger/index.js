const { loadFilesSync } = require('@graphql-tools/load-files')
const { mergeTypeDefs } = require('@graphql-tools/merge')
const { print } = require('graphql')
const fs = require('fs')
const path = require('path')
 
const schemaDirectory = path.join(__dirname, '..', '**', 'schema.graphql');
const loadedFiles  = loadFilesSync(schemaDirectory);
const typeDefs = mergeTypeDefs(loadedFiles)
const printedTypeDefs = print(typeDefs)

fs.writeFileSync(path.join(__dirname, '..', 'unified-schema.graphql'), printedTypeDefs);