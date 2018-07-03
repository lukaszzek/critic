# -*- mode: python; encoding: utf-8 -*-
#
# Copyright 2014 the Critic contributors, Opera Software ASA
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

import sys
import psycopg2
import json
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--uid", type=int)
parser.add_argument("--gid", type=int)

arguments = parser.parse_args()

os.setgid(arguments.gid)
os.setuid(arguments.uid)

data = json.load(sys.stdin)

db = psycopg2.connect(database="critic")
cursor = db.cursor()

try:
    # Check if the 'origin' column already exists.
    cursor.execute("SELECT origin FROM reviews")
except psycopg2.ProgrammingError:
    # Seems it doesn't.
    db.rollback()
else:
    sys.exit(0)

# Add the reviews.origin column.
cursor.execute(
    """ALTER TABLE reviews
         ADD origin INTEGER REFERENCES branches ON DELETE SET NULL""")

# Copy the information in branches.review over to reviews.origin.
cursor.execute("""SELECT id, review
                    FROM branches
                   WHERE review IS NOT NULL""")
rows = cursor.fetchall()
cursor.executemany("""UPDATE reviews
                         SET origin=%s
                       WHERE id=%s""",
                   rows)

# Drop the old branches.review column.
cursor.execute("""ALTER TABLE branches DROP review""")

db.commit()
db.close()


def runtime_migrate():
    print "Hello"

