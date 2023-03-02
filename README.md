# odd-collector-aws-stack

The purpose of this plugin is to create the new adapter that collects and parses the current AWS stack metadata using open-source Former2 library. 

The structure was mainly forked from odd-collector. Suitable for merge, though, Former2 requires new massive node.js dependencies, it was decided to leave this adapter outside of odd-collector until the decision is made to involve this adapter into a larger pipeline with future plugins that scan user's data lineage using opentelemetry. 

That would allow to compare the actual lineage with permissions given to:

1. highlight overabundant permissions given to a scanned resource;
2. create a map of user's resources to show which resources are used and which are idle
3. extract metadata information that could be potentially used in opentelemetry plugin to identify the resource been invoked

# installation

Basic installation is the same as for odd-collector project https://github.com/opendatadiscovery/odd-collector 

Installation of nvm, npm and former2 is included into Dockerfile and does not require any manual actions