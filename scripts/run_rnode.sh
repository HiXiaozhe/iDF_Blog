#!/bin/bash
cd ../RChain/rnode0
rm -rf blockstorage
rm -rf casperbuffer
rm -rf dagstorage
rm -rf deploystorage
rm -rf eval
rm -rf rspace
rm -rf node.certificate.pem
rm -rf node.key.pem
rm -rf rnode.log

cd ..
rchain-release/bin/rnode run --config-file config.conf